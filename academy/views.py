# academy/views.py
import base64
from pathlib import Path
from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.views import View, generic
from django.views.decorators.http import require_POST

from weasyprint import HTML

from .forms import GoalForm, CommentForm
from .ai_services import generate_pathway_outline, generate_module_content, fetch_youtube_video
from .models import (
    LearningPathway,
    PathwayModule,
    ModuleStep,
    Badge,
    UserBadge,
    Comment,
)


# -------------------------------
# Public & Dashboard Views
# -------------------------------
class PublicPathwayDetailView(generic.DetailView):
    model = LearningPathway
    template_name = "academy/public_pathway_detail.html"
    context_object_name = "pathway"


class AcademyDashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "academy/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Load user's pathways and mark completion state for template
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
            goal, location = form.cleaned_data["goal"], form.cleaned_data["location"]
            try:
                pathway_outline = generate_pathway_outline(goal, location)
            except Exception:
                pathway_outline = None

            # Accept 'curriculum' key from older AI responses
            if pathway_outline and "curriculum" in pathway_outline:
                pathway_outline["modules"] = pathway_outline.pop("curriculum")

            if pathway_outline and "modules" in pathway_outline:
                pathway = LearningPathway.objects.create(
                    user=request.user, goal=goal, location=location
                )
                for order, module_data in enumerate(pathway_outline.get("modules", [])):
                    module = PathwayModule.objects.create(
                        pathway=pathway,
                        title=module_data.get("title", ""),
                        youtube_search_query=module_data.get("youtube_search_query", ""),
                        order=order,
                    )
                    for step_order, step_title in enumerate(module_data.get("steps", [])):
                        ModuleStep.objects.create(
                            module=module, title=step_title, order=step_order
                        )
                messages.success(request, _("Your personalized learning pathway has been generated!"))
                return redirect("academy:pathway-detail", pk=pathway.pk)
            else:
                messages.error(
                    request,
                    _("Sorry, we couldn't generate a pathway. Please try a different goal."),
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
        context["is_pathway_complete"] = not pathway.modules.filter(is_completed=False).exists()

        unlocked_module = pathway.modules.filter(is_completed=False).order_by("order").first()
        if unlocked_module and not unlocked_module.content_generated:
            previous_module = (
                pathway.modules.filter(order__lt=unlocked_module.order).order_by("-order").first()
            )
            used_video_ids = {
                url.split("v=")[-1]
                for url in pathway.modules.exclude(video_url__isnull=True)
                .exclude(video_url__exact="")
                .values_list("video_url", flat=True)
                if "v=" in url
            }
            try:
                module_content = generate_module_content(
                    unlocked_module.title, previous_module.title if previous_module else None
                )
            except Exception:
                module_content = unlocked_module.written_content or ""

            try:
                video_url, _ = fetch_youtube_video(unlocked_module.youtube_search_query, used_video_ids)
            except Exception:
                video_url = unlocked_module.video_url or ""

            unlocked_module.written_content = module_content
            unlocked_module.video_url = video_url
            unlocked_module.content_generated = True
            unlocked_module.save()

        context["unlocked_module"] = unlocked_module
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
        messages.success(request, _("Your comment has been deleted."))
        return super().post(request, *args, **kwargs)


# -------------------------------
# Module Completion
# -------------------------------
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
    """
    Generates a PDF certificate using WeasyPrint.
    Passes first_name / last_name separately and embeds signature as base64.
    """

    def get(self, request, pk):
        pathway = get_object_or_404(LearningPathway, pk=pk, user=request.user)

        # Only allow download when pathway is complete
        if not all(module.is_completed for module in pathway.modules.all()):
            raise Http404("Pathway is not yet complete.")

        # Load signature image and encode to base64 (safe fallback to empty string)
        signature_data_uri = ""
        try:
            signature_file = Path(settings.BASE_DIR) / "core" / "static" / "img" / "signature.png"
            if signature_file.exists():
                with open(signature_file, "rb") as f:
                    signature_base64 = base64.b64encode(f.read()).decode("utf-8")
                signature_data_uri = f"data:image/png;base64,{signature_base64}"
        except Exception:
            signature_data_uri = ""

        # Prepare name components
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
        html = HTML(string=html_string, base_url=request.build_absolute_uri())

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="Kiri_ng_Certificate_{pathway.slug}.pdf"'
        html.write_pdf(target=response)
        return response
