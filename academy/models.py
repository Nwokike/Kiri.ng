from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class LearningPathway(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pathways')
    goal = models.TextField(_("User's Goal"))
    location = models.CharField(_("Location"), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Pathway for {self.user.username} in {self.location}"

class PathwayModule(models.Model):
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(_("Module Title"), max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    written_content = models.TextField(_("Original Written Content"), blank=True)
    video_url = models.URLField(_("Supplementary Video URL"), blank=True, null=True)
    content_generated = models.BooleanField(default=False)
    youtube_search_query = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['order']
    def __str__(self):
        return f"{self.order}: {self.title}"

class ModuleStep(models.Model):
    module = models.ForeignKey(PathwayModule, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(_("Step Title"), max_length=255)
    order = models.PositiveIntegerField(default=0)
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

class Comment(models.Model):
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] 
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f'Comment by {self.author.username} on {self.pathway.title}'