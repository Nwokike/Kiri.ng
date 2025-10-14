from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

class LearningPathway(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_pathways')
    category = models.ForeignKey('marketplace.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='academy_pathways')
    goal = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.goal)
        super().save(*args, **kwargs)

    # --- THIS IS THE FIX: Added the missing method ---
    def get_absolute_url(self):
        return reverse('academy:pathway-detail', kwargs={'pk': self.pk})

    def get_public_url(self):
        return reverse('academy:public-pathway-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return f"Pathway for {self.user.username}: {self.goal}"

class PathwayModule(models.Model):
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(_("Module Title"), max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    written_content = models.TextField(_("Written Content"), blank=True)
    video_url = models.URLField(_("Primary Video URL"), blank=True, null=True)
    content_generated = models.BooleanField(default=False)
    youtube_search_query = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self): 
        return f"{self.order}: {self.title}"


class ModuleVideo(models.Model):
    module = models.ForeignKey(PathwayModule, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(_("Video Title"), max_length=255)
    video_url = models.URLField(_("Video URL"))
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(_("Video Description"), blank=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - Video {self.order + 1}"


class ModuleQuestion(models.Model):
    module = models.ForeignKey(PathwayModule, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academy_questions')
    question_text = models.TextField(_("Question"))
    ai_answer = models.TextField(_("AI-Generated Answer"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Question by {self.user.username} on {self.module.title}"

class ModuleStep(models.Model):
    module = models.ForeignKey(PathwayModule, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(_("Step Title"), max_length=255)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self): return f"Step {self.order} for {self.module.title}"

class Badge(models.Model):
    title = models.CharField(_("Badge Title"), max_length=100, unique=True)
    description = models.TextField(_("Badge Description"))
    icon = models.CharField(max_length=50, blank=True) # Changed from icon_svg for simplicity
    def __str__(self): return self.title

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges') # Changed related_name
    awarded_at = models.DateTimeField(auto_now_add=True) # Renamed from earned_at
    class Meta:
        unique_together = ('user', 'badge')
    def __str__(self): return f"{self.user.username} earned {self.badge.title}"

class ModuleQuiz(models.Model):
    """Multiple choice quiz for module completion validation"""
    module = models.OneToOneField(PathwayModule, on_delete=models.CASCADE, related_name='quiz')
    question = models.TextField(_("Quiz Question"))
    option_a = models.CharField(_("Option A"), max_length=500)
    option_b = models.CharField(_("Option B"), max_length=500)
    option_c = models.CharField(_("Option C"), max_length=500)
    option_d = models.CharField(_("Option D"), max_length=500)
    correct_answer = models.CharField(_("Correct Answer"), max_length=1, choices=[
        ('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')
    ])
    
    def __str__(self):
        return f"Quiz for {self.module.title}"

class Comment(models.Model):
    pathway = models.ForeignKey(LearningPathway, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academy_comments') # Added related_name
    body = models.TextField(_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at'] # Changed to descending
    def __str__(self):
        # --- THIS IS THE FIX: Changed pathway.title to pathway.goal ---
        return f'Comment by {self.author.username} on {self.pathway.goal}'