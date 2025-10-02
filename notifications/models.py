from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.URLField(blank=True, null=True, help_text=_("Link to the relevant page"))
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:30]}"