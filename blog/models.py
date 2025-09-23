from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', _('Draft')
        PUBLISHED = 'PB', _('Published')

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    # --- THIS IS THE FIX: Removed the "Text" label ---
    body = CKEditor5Field(config_name='default')
    
    header_image = models.ImageField(upload_to='post_headers/', blank=True, null=True, help_text=_("Optional: Upload an image that will appear at the top of your post."))
    publish = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self): return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'