from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SEOSettings(models.Model):
    """SEO settings - only one instance should exist"""
    auto_submit_to_indexnow = models.BooleanField(
        default=True,
        help_text=_("Automatically submit new/updated content to IndexNow")
    )
    indexnow_key = models.CharField(
        max_length=100,
        blank=True,
        help_text=_("IndexNow API key (auto-generated if empty)")
    )
    last_sitemap_ping = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Last time sitemap was pinged to search engines")
    )
    last_indexnow_submission = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Last IndexNow submission time")
    )
    
    class Meta:
        verbose_name = _("SEO Settings")
        verbose_name_plural = _("SEO Settings")
    
    def __str__(self):
        return "SEO Settings"
    
    def save(self, *args, **kwargs):
        if not self.pk and SEOSettings.objects.exists():
            raise ValueError("Only one SEO Settings instance is allowed")
        return super().save(*args, **kwargs)


class IndexNowSubmission(models.Model):
    """Track IndexNow submissions"""
    url = models.URLField(max_length=500)
    submitted_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    response_code = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = _("IndexNow Submission")
        verbose_name_plural = _("IndexNow Submissions")
    
    def __str__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.url} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"


class SupportTicket(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        RESOLVED = 'RESOLVED', _('Resolved')
        CLOSED = 'CLOSED', _('Closed')
    
    class Category(models.TextChoices):
        TECHNICAL = 'TECH', _('Technical Issue')
        ACCOUNT = 'ACCT', _('Account Issue')
        PAYMENT = 'PAY', _('Payment Issue')
        FEATURE = 'FEAT', _('Feature Request')
        BOOKING = 'BOOK', _('Booking Issue')
        OTHER = 'OTHER', _('Other')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets', null=True, blank=True)
    email = models.EmailField(help_text=_("Contact email for ticket updates"))
    category = models.CharField(max_length=15, choices=Category.choices, default=Category.OTHER)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text=_("Internal notes for admin"))
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at', 'status'])]
        verbose_name = _("Support Ticket")
        verbose_name_plural = _("Support Tickets")
    
    def __str__(self):
        return f"Ticket #{self.pk} - {self.subject}"
