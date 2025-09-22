from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import GoalForm, CommentForm
from .ai_services import generate_pathway_outline, generate_module_content, fetch_youtube_video
from .models import LearningPathway, PathwayModule, ModuleStep, Badge, UserBadge, Comment

# --- THIS IS THE MISSING VIEW THAT FIXES THE CRASH ---
class AcademyDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'academy/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get the user's specific pathway
        my_pathway = LearningPathway.objects.filter(user=user).first()
        context['my_pathway'] = my_pathway
        
        # Get the user's earned badges
        context['my_badges'] = UserBadge.objects.filter(user=user)
        
        # Get the 5 most recent comments from the whole community
        context['recent_comments'] = Comment.objects.order_by('-created_at')[:5]
        
        # If the user has no pathway, include the creation form
        if not my_pathway:
            context['goal_form'] = GoalForm()
            
        return context
# --- END OF THE NEW VIEW ---


class PathwayListView(generic.ListView):
    model = LearningPathway
    template_name = 'academy/pathway_list.html'
    context_object_name = 'pathways'
    queryset = LearningPathway.objects.all().order_by('-created_at')

class CreatePathwayView(LoginRequiredMixin, View):
    template_name = 'academy/create_pathway.html'

    def get(self, request, *args, **kwargs):
        pathway = LearningPathway.objects.filter(user=request.user).first()
        if pathway:
            messages.info(request, _("You already have a learning pathway."))
            return redirect('academy:pathway-detail', pk=pathway.pk)
        
        form = GoalForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.cleaned_data['goal']
            location = form.cleaned_data['location']
            
            try:
                pathway_outline = generate_pathway_outline(goal, location)
            except Exception as e:
                pathway_outline = None

            if pathway_outline and 'curriculum' in pathway_outline:
                pathway_outline['modules'] = pathway_outline.pop('curriculum')

            if pathway_outline and 'modules' in pathway_outline:
                pathway = LearningPathway.objects.create(user=request.user, goal=goal, location=location)
                for module_order, module_data in enumerate(pathway_outline.get('modules', [])):
                    module = PathwayModule.objects.create(
                        pathway=pathway,
                        title=module_data.get('title', 'Untitled Module'),
                        youtube_search_query=module_data.get('youtube_search_query', ''),
                        order=module_order
                    )
                    for step_order, step_title in enumerate(module_data.get('steps', [])):
                        ModuleStep.objects.create(module=module, title=step_title, order=step_order)
                messages.success(request, _("Your personalized learning pathway has been generated!"))
                return redirect('academy:pathway-detail', pk=pathway.pk)
            else:
                messages.error(request, _("Sorry, we couldn't generate a pathway. Please try a different goal."))
        else:
            messages.error(request, _("Please correct the errors below."))
        return render(request, self.template_name, {'form': form})

class PathwayDetailView(LoginRequiredMixin, generic.DetailView):
    model = LearningPathway
    template_name = 'academy/pathway_detail.html'
    context_object_name = 'pathway'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pathway = self.object
        context['comments'] = pathway.comments.all().order_by('created_at')
        context['comment_form'] = CommentForm()
        unlocked_module = pathway.modules.filter(is_completed=False).order_by('order').first()
        
        if unlocked_module and not unlocked_module.content_generated:
            previous_module = pathway.modules.filter(order__lt=unlocked_module.order).order_by('-order').first()
            previous_module_title = previous_module.title if previous_module else None
            used_video_ids = set(pathway.modules.exclude(video_url__isnull=True).exclude(video_url__exact='').values_list('video_url', flat=True))
            used_ids = {url.split('v=')[-1] for url in used_video_ids if 'v=' in url}
            module_content = generate_module_content(unlocked_module.title, previous_module_title)
            video_url, new_video_id = fetch_youtube_video(unlocked_module.youtube_search_query, used_ids)

            unlocked_module.written_content = module_content
            unlocked_module.video_url = video_url
            unlocked_module.content_generated = True
            unlocked_module.save()

        context['unlocked_module'] = unlocked_module
        return context

    def post(self, request, *args, **kwargs):
        pathway = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pathway = pathway
            comment.author = request.user
            comment.save()
            messages.success(request, _("Your comment has been added."))
            return redirect('academy:pathway-detail', pk=pathway.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            messages.error(request, _("There was an error with your comment."))
            return self.render_to_response(context)

@login_required
def complete_module(request, module_id):
    module = get_object_or_404(PathwayModule, id=module_id, pathway__user=request.user)
    if request.method == 'POST':
        module.is_completed = True
        module.save()

        pathway = module.pathway
        if not pathway.modules.filter(is_completed=False).exists():
            try:
                badge = Badge.objects.get(title="Academy Graduate")
                UserBadge.objects.get_or_create(user=request.user, badge=badge)
                messages.success(request, f"Congratulations! You've completed the entire pathway and earned the '{badge.title}' badge!")
            except Badge.DoesNotExist:
                messages.info(request, "You've completed the entire pathway!")
        else:
             messages.success(request, f"Module '{module.title}' completed! The next module is unlocked.")

        return redirect('academy:pathway-detail', pk=pathway.pk)
    
    return redirect('academy:pathway-detail', pk=module.pathway.pk)