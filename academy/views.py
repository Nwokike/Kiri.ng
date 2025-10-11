import base64
import logging
from pathlib import Path
from datetime import date

from django.conf import settings

logger = logging.getLogger(__name__)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View, generic
from django.views.decorators.http import require_POST

from weasyprint import HTML

from .forms import GoalForm, CommentForm, QuestionForm
from .ai_services import (
    generate_pathway_outline,
    generate_module_content,
    fetch_multiple_youtube_videos,
    answer_module_question
)
from .models import (
    LearningPathway,
    PathwayModule,
    ModuleStep,
    ModuleVideo,
    ModuleQuestion,
    Badge,
    UserBadge,
    Comment,
)
from notifications.models import Notification  # Added import


# -------------------------------
# Public & Dashboard Views
# -------------------------------
class AcademyHomeView(generic.TemplateView):
    template_name = "academy/academy_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_pathways"] = LearningPathway.objects.all().order_by("-created_at")[:5]
        return context


class PublicPathwayDetailView(generic.DetailView):
    model = LearningPathway
    template_name = "academy/public_pathway_detail.html"
    context_object_name = "pathway"


class AcademyDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "academy/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        my_pathways = LearningPathway.objects.filter(user=user).order_by("-created_at")
        for pathway in my_pathways:
            pathway.is_complete = all(m.is_completed for m in pathway.modules.all())

        context["my_pathways"] = my_pathways
        context["my_badges"] = UserBadge.objects.filter(user=user)
        context["recent_comments"] = Comment.objects.select_related("author", "pathway").order_by("-created_at")[:5]

        if not my_pathways.exists():
            context["goal_form"] = GoalForm()

        context["can_create_new_pathway"] = (
            not my_pathways.exists() or user.profile.successful_referrals_count > 0
        )
        return context


class PathwayListView(generic.ListView):
    model = LearningPathway
    template_name = "academy/pathway_list.html"
    context_object_name = "pathways"
    queryset = LearningPathway.objects.all().order_by("-created_at")


# -------------------------------
# Pathway Creation
# -------------------------------
class CreatePathwayView(LoginRequiredMixin, View):
    template_name = "academy/create_pathway.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        my_pathway = LearningPathway.objects.filter(user=user).first()

        if my_pathway and user.profile.successful_referrals_count == 0:
            messages.warning(
                request, _("You must refer one user to create a new Learning Pathway.")
            )
            return redirect("academy:dashboard")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": GoalForm()})

    def post(self, request, *args, **kwargs):
        form = GoalForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            goal, location = form.cleaned_data["goal"], form.cleaned_data["location"]
            
            try:
                pathway_outline = generate_pathway_outline(goal, location, category.name if category else None)
            except Exception as e:
                logger.error(f"Error generating pathway: {e}")
                pathway_outline = None

            if pathway_outline and "modules" in pathway_outline:
                from .forms import BUSINESS_GOALS
                goal_display = dict(BUSINESS_GOALS).get(goal, goal)
                goal_text = f"{category.name}: {goal_display}"
                
                pathway = LearningPathway.objects.create(
                    user=request.user,
                    category=category,
                    goal=goal_text,
                    location=location
                )
                
                for order, module_data in enumerate(pathway_outline.get("modules", [])):
                    module = PathwayModule.objects.create(
                        pathway=pathway,
                        title=module_data.get("title", ""),
                        youtube_search_query=module_data.get("youtube_search_query", ""),
                        order=order,
                    )
                    # ModuleStep creation removed - steps not displayed in UI
                    # for step_order, step_title in enumerate(module_data.get("steps", [])):
                    #     ModuleStep.objects.create(module=module, title=step_title, order=step_order)
                
                messages.success(request, _("Your personalized learning pathway has been generated! Start learning now."))
                return redirect("academy:pathway-detail", pk=pathway.pk)
            else:
                messages.error(
                    request,
                    _("Sorry, we couldn't generate a pathway. Please try again or contact support."),
                )
        return render(request, self.template_name, {"form": form})


# -------------------------------
# Pathway Detail
# -------------------------------
class PathwayDetailView(LoginRequiredMixin, generic.DetailView):
    model = LearningPathway
    template_name = "academy/pathway_detail.html"
    context_object_name = "pathway"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pathway = self.object

        context["comments"] = pathway.comments.all().order_by("created_at")
        context["comment_form"] = CommentForm()
        context["question_form"] = QuestionForm()
        context["is_pathway_complete"] = not pathway.modules.filter(is_completed=False).exists()

        unlocked_module = pathway.modules.filter(is_completed=False).order_by("order").first()
        if unlocked_module and not unlocked_module.content_generated:
            previous_module = (
                pathway.modules.filter(order__lt=unlocked_module.order).order_by("-order").first()
            )
            
            used_video_ids = set()
            for module in pathway.modules.all():
                for video in module.videos.all():
                    if "v=" in video.video_url:
                        used_video_ids.add(video.video_url.split("v=")[-1])
            
            try:
                videos = fetch_multiple_youtube_videos(
                    unlocked_module.youtube_search_query,
                    num_videos=4,
                    used_ids=used_video_ids
                )
                
                video_titles = [v['title'] for v in videos]
                module_content = generate_module_content(
                    unlocked_module.title,
                    previous_module.title if previous_module else None,
                    video_titles=video_titles
                )
                
                if videos:
                    unlocked_module.video_url = videos[0]['url']
                    unlocked_module.save()
                    
                    for idx, video in enumerate(videos):
                        ModuleVideo.objects.create(
                            module=unlocked_module,
                            title=video['title'],
                            video_url=video['url'],
                            description=video['description'],
                            order=idx
                        )
            except Exception as e:
                logger.error(f"Error generating content/videos: {e}")
                module_content = unlocked_module.written_content or "Content could not be generated. Please refresh the page."

            unlocked_module.written_content = module_content
            unlocked_module.content_generated = True
            unlocked_module.save()

        context["unlocked_module"] = unlocked_module
        
        if unlocked_module:
            context["module_videos"] = unlocked_module.videos.all()
            context["module_questions"] = unlocked_module.questions.filter(user=self.request.user).order_by('-created_at')
        
        return context

    def post(self, request, *args, **kwargs):
        pathway = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pathway = pathway
            comment.author = request.user
            comment.save()

            # --- CREATE NOTIFICATION ---
            if pathway.user != request.user:
                Notification.objects.create(
                    recipient=pathway.user,
                    message=_(f"{request.user.username} commented on your pathway: '{pathway.goal}'"),
                    link=pathway.get_absolute_url()
                )

            messages.success(request, _("Your comment has been posted."))
            return redirect("academy:pathway-detail", pk=pathway.pk)

        context = self.get_context_data()
        context["comment_form"] = form
        messages.error(request, _("There was an error with your comment."))
        return self.render_to_response(context)


# -------------------------------
# Comment Views
# -------------------------------
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment_form.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.pathway.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.pathway.get_absolute_url()

    def post(self, request, *args, **kwargs):
        messages.success(self.request, _("Your comment has been deleted."))
        return super().post(request, *args, **kwargs)


# -------------------------------
# Module Completion
# -------------------------------
@login_required
@require_POST
def ask_question(request, module_id):
    """Handle AI question answering for a module."""
    module = get_object_or_404(PathwayModule, id=module_id)
    
    if request.POST.get('question'):
        question_text = request.POST.get('question').strip()
        
        if len(question_text) < 10:
            messages.error(request, _("Please ask a more detailed question (at least 10 characters)."))
            return redirect("academy:pathway-detail", pk=module.pathway.pk)
        
        try:
            ai_answer = answer_module_question(
                question_text,
                module.title,
                module.written_content
            )
            
            ModuleQuestion.objects.create(
                module=module,
                user=request.user,
                question_text=question_text,
                ai_answer=ai_answer,
                answered=True
            )
            
            messages.success(request, _("Your question has been answered by the AI instructor!"))
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            messages.error(request, _("Sorry, couldn't generate an answer. Please try again."))
    
    return redirect("academy:pathway-detail", pk=module.pathway.pk)


@login_required
@require_POST
def complete_module(request, module_id):
    module = get_object_or_404(PathwayModule, id=module_id, pathway__user=request.user)
    answer = request.POST.get("validation_answer", "").strip()

    if len(answer) < 50:
        messages.error(
            request,
            _("Your answer is too short. Please describe what you learned in more detail to complete the module."),
        )
        return redirect("academy:pathway-detail", pk=module.pathway.pk)

    module.is_completed = True
    module.save()

    pathway = module.pathway
    if not pathway.modules.filter(is_completed=False).exists():
        try:
            badge = Badge.objects.get(title="Academy Graduate")
            UserBadge.objects.get_or_create(user=request.user, badge=badge)
            messages.success(
                request,
                _("Congratulations! You've completed the entire pathway and earned the '{badge.title}' badge!").format(
                    badge=badge
                ),
            )
        except Badge.DoesNotExist:
            messages.info(request, _("You've completed the entire pathway!"))
    else:
        messages.success(
            request, _("Module '{module.title}' completed! The next module is unlocked.").format(module=module)
        )

    return redirect("academy:pathway-detail", pk=pathway.pk)


# -------------------------------
# Certificate Download
# -------------------------------
class DownloadCertificateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        pathway = get_object_or_404(LearningPathway, pk=pk, user=request.user)

        if not all(module.is_completed for module in pathway.modules.all()):
            raise Http404("Pathway is not yet complete.")

        signature_data_uri = ""
        try:
            signature_file = Path(settings.BASE_DIR) / "core" / "static" / "img" / "signature.png"
            if signature_file.exists():
                with open(signature_file, "rb") as f:
                    signature_base64 = base64.b64encode(f.read()).decode("utf-8")
                signature_data_uri = f"data:image/png;base64,{signature_base64}"
        except Exception:
            signature_data_uri = ""

        first_name = (request.user.first_name or "").strip()
        last_name = (request.user.last_name or "").strip()
        full_name = (request.user.get_full_name() or request.user.username).strip()

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "pathway_goal": pathway.goal,
            "modules": pathway.modules.all(),
            "completion_date": date.today().strftime("%B %d, %Y"),
            "signature_path": signature_data_uri,
        }

        html_string = render_to_string("academy/certificate.html", context)
        
        try:
            # Attempt to generate PDF certificate
            html = HTML(string=html_string, base_url=request.build_absolute_uri())
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="Kiri_ng_Certificate_{pathway.slug}.pdf"'
            html.write_pdf(target=response)
            logger.info(f"Successfully generated PDF certificate for pathway {pathway.slug}")
            return response
        except Exception as e:
            # Fallback to HTML certificate if PDF generation fails
            logger.error(f"PDF certificate generation failed: {str(e)}")
            messages.warning(
                request, 
                _("PDF generation temporarily unavailable. Displaying certificate in browser instead.")
            )
            response = HttpResponse(html_string, content_type="text/html")
            return response
