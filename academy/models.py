from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class LearningPathway(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathways')
    goal = models.TextField(_("User's Goal"))
    generated_modules = models.JSONField(default=list, help_text=_("The raw AI-generated module structure."))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pathway for {self.user.username}: {self.goal[:50]}..."

class PathwayModule(models.Model):
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(_("Module Title"), max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}: {self.title}"

class ModuleStep(models.Model):
    STEP_TYPES = (('video', _('Video')), ('article', _('Article')), ('task', _('Practical Task')))
    module = models.ForeignKey(PathwayModule, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(_("Step Title"), max_length=255)
    content_url = models.URLField(_("Content URL"), blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    step_type = models.CharField(max_length=10, choices=STEP_TYPES, default='video')
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order} for {self.module.title}"

class Badge(models.Model):
    title = models.CharField(_("Badge Title"), max_length=100, unique=True)
    description = models.TextField(_("Badge Description"))
    icon_svg = models.TextField(_("Icon SVG Code"), help_text=_("Paste the SVG code for the badge icon here."))

    def __str__(self):
        return self.title

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='earned_by')
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.title}"