from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST # <-- Import this

from .forms import GoalForm, CommentForm
from .ai_services import generate_pathway_outline, generate_module_content, fetch_youtube_video
from .models import LearningPathway, PathwayModule, ModuleStep, Badge, UserBadge, Comment

class PublicPathwayDetailView(generic.DetailView):
    model = LearningPathway
    template_name = 'academy/public_pathway_detail.html'
    context_object_name = 'pathway'

class AcademyDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'academy/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        my_pathway = LearningPathway.objects.filter(user=user).first()
        context['my_pathway'], context['my_badges'] = my_pathway, UserBadge.objects.filter(user=user)
        context['recent_comments'] = Comment.objects.order_by('-created_at')[:5]
        if not my_pathway:
            context['goal_form'] = GoalForm()
        return context

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
        return render(request, self.template_name, {'form': GoalForm()})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal, location = form.cleaned_data['goal'], form.cleaned_data['location']
            try: pathway_outline = generate_pathway_outline(goal, location)
            except Exception: pathway_outline = None
            if pathway_outline and 'curriculum' in pathway_outline: pathway_outline['modules'] = pathway_outline.pop('curriculum')
            if pathway_outline and 'modules' in pathway_outline:
                pathway = LearningPathway.objects.create(user=request.user, goal=goal, location=location)
                for order, module_data in enumerate(pathway_outline.get('modules', [])):
                    module = PathwayModule.objects.create(pathway=pathway, title=module_data.get('title', ''), youtube_search_query=module_data.get('youtube_search_query', ''), order=order)
                    for step_order, step_title in enumerate(module_data.get('steps', [])):
                        ModuleStep.objects.create(module=module, title=step_title, order=step_order)
                messages.success(request, _("Your personalized learning pathway has been generated!"))
                return redirect('academy:pathway-detail', pk=pathway.pk)
            else: messages.error(request, _("Sorry, we couldn't generate a pathway. Please try a different goal."))
        return render(request, self.template_name, {'form': form})

class PathwayDetailView(LoginRequiredMixin, generic.DetailView):
    model = LearningPathway
    template_name = 'academy/pathway_detail.html'
    context_object_name = 'pathway'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pathway = self.object
        context['comments'], context['comment_form'] = pathway.comments.all().order_by('created_at'), CommentForm()
        unlocked_module = pathway.modules.filter(is_completed=False).order_by('order').first()
        if unlocked_module and not unlocked_module.content_generated:
            previous_module = pathway.modules.filter(order__lt=unlocked_module.order).order_by('-order').first()
            used_video_ids = {url.split('v=')[-1] for url in pathway.modules.exclude(video_url__isnull=True).exclude(video_url__exact='').values_list('video_url', flat=True) if 'v=' in url}
            module_content = generate_module_content(unlocked_module.title, previous_module.title if previous_module else None)
            video_url, _ = fetch_youtube_video(unlocked_module.youtube_search_query, used_video_ids)
            unlocked_module.written_content, unlocked_module.video_url, unlocked_module.content_generated = module_content, video_url, True
            unlocked_module.save()
        context['unlocked_module'] = unlocked_module
        return context
    def post(self, request, *args, **kwargs):
        pathway = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pathway, comment.author = pathway, request.user
            comment.save()
            messages.success(request, _("Your comment has been added."))
            return redirect('academy:pathway-detail', pk=pathway.pk)
        context = self.get_context_data()
        context['comment_form'] = form
        messages.error(request, _("There was an error with your comment."))
        return self.render_to_response(context)
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'academy/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.pathway.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'academy/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return self.object.pathway.get_absolute_url()

    # --- THIS IS THE FIX: Add the success message ---
    def post(self, request, *args, **kwargs):
        messages.success(self.request, _("Your comment has been deleted."))
        return super().post(request, *args, **kwargs)

@login_required
@require_POST # <-- Add this decorator to ensure it only accepts POST requests
def complete_module(request, module_id):
    module = get_object_or_404(PathwayModule, id=module_id, pathway__user=request.user)
    # --- THIS IS THE FIX: We now check the user's answer before completing ---
    answer = request.POST.get('validation_answer', '').strip()
    if len(answer) < 50: # Check if the answer is substantial
        messages.error(request, _("Your answer is too short. Please describe what you learned in more detail to complete the module."))
        return redirect('academy:pathway-detail', pk=module.pathway.pk)

    module.is_completed = True
    module.save()
    pathway = module.pathway
    if not pathway.modules.filter(is_completed=False).exists():
        try:
            badge = Badge.objects.get(title="Academy Graduate")
            UserBadge.objects.get_or_create(user=request.user, badge=badge)
            messages.success(request, _("Congratulations! You've completed the entire pathway and earned the '{badge.title}' badge!").format(badge=badge))
        except Badge.DoesNotExist:
            messages.info(request, _("You've completed the entire pathway!"))
    else:
        messages.success(request, _("Module '{module.title}' completed! The next module is unlocked.").format(module=module))
    return redirect('academy:pathway-detail', pk=pathway.pk)