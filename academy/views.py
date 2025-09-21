from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import GoalForm
from .ai_services import generate_pathway_outline, generate_module_content, fetch_youtube_video
from .models import LearningPathway, PathwayModule, ModuleStep, Badge, UserBadge

class AcademyDashboardView(LoginRequiredMixin, View):
    template_name = 'academy/dashboard.html'

    def get(self, request, *args, **kwargs):
        pathway = LearningPathway.objects.filter(user=request.user).first()
        if pathway:
            return redirect('academy:pathway-detail', pk=pathway.pk)
        form = GoalForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.cleaned_data['goal']
            location = form.cleaned_data['location']
            pathway_outline = generate_pathway_outline(goal, location)

            if pathway_outline and 'modules' in pathway_outline:
                pathway = LearningPathway.objects.create(user=request.user, goal=goal, location=location)
                for module_order, module_data in enumerate(pathway_outline.get('modules', [])):
                    module = PathwayModule.objects.create(
                        pathway=pathway,
                        title=module_data.get('title', 'Untitled Module'),
                        youtube_search_query=module_data.get('youtube_search_query', ''),
                        order=module_order
                    )
                    # --- THIS LOGIC IS NOW CORRECT ---
                    # It correctly loops through the simple list of step strings.
                    for step_order, step_title in enumerate(module_data.get('steps', [])):
                        ModuleStep.objects.create(
                            module=module,
                            title=step_title,
                            order=step_order
                        )
                messages.success(request, _("Your personalized learning pathway outline has been generated!"))
                return redirect('academy:pathway-detail', pk=pathway.pk)
            else:
                messages.error(request, _("Sorry, we couldn't generate a pathway outline. Please try a different goal."))
        else:
            messages.error(request, _("Please correct the errors below."))
        return render(request, self.template_name, {'form': form})

class PathwayDetailView(LoginRequiredMixin, generic.DetailView):
    model = LearningPathway
    template_name = 'academy/pathway_detail.html'
    context_object_name = 'pathway'

    def get_queryset(self):
        return LearningPathway.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pathway = self.object
        unlocked_module = pathway.modules.filter(is_completed=False).order_by('order').first()
        
        if unlocked_module and not unlocked_module.content_generated:
            print(f"Content for module '{unlocked_module.title}' not found. Generating now...")
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
            print("Content generation complete and saved.")

        context['unlocked_module'] = unlocked_module
        return context

@login_required
def complete_module(request, module_id):
    module = get_object_or_404(PathwayModule, id=module_id, pathway__user=request.user)
    if request.method == 'POST':
        module.is_completed = True
        module.save()

        pathway = module.pathway
        if not pathway.modules.filter(is_completed=False).exists():
            print("Pathway complete! Attempting to award badge...")
            try:
                badge = Badge.objects.get(title="Academy Graduate")
                UserBadge.objects.get_or_create(user=request.user, badge=badge)
                messages.success(request, f"Congratulations! You've completed the entire pathway and earned the '{badge.title}' badge!")
            except Badge.DoesNotExist:
                print("CRITICAL: The 'Academy Graduate' badge does not exist in the admin panel.")
                messages.info(request, "You've completed the entire pathway!")
        else:
             messages.success(request, f"Module '{module.title}' completed! The next module is unlocked.")

        return redirect('academy:pathway-detail', pk=pathway.pk)
    
    return redirect('academy:pathway-detail', pk=module.pathway.pk)