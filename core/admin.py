from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from .models import SEOSettings, IndexNowSubmission, SupportTicket
from .indexnow import submit_to_indexnow, ping_search_engines
from django.contrib.sites.models import Site


@admin.register(SEOSettings)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'auto_submit_to_indexnow', 'last_sitemap_ping', 'last_indexnow_submission']
    fieldsets = (
        ('IndexNow Settings', {
            'fields': ('auto_submit_to_indexnow', 'indexnow_key', 'last_indexnow_submission')
        }),
        ('Sitemap Settings', {
            'fields': ('last_sitemap_ping',)
        }),
    )
    readonly_fields = ('last_sitemap_ping', 'last_indexnow_submission')
    
    actions = ['ping_sitemap_to_search_engines', 'submit_all_urls_to_indexnow']
    
    def has_add_permission(self, request):
        if SEOSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    @admin.action(description='Ping sitemap to search engines (Google, Bing)')
    def ping_sitemap_to_search_engines(self, request, queryset):
        try:
            ping_search_engines()
            for obj in queryset:
                obj.last_sitemap_ping = timezone.now()
                obj.save()
            self.message_user(request, "Successfully pinged sitemap to search engines!", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error pinging sitemap: {e}", messages.ERROR)
    
    @admin.action(description='Submit sitemap URLs to IndexNow')
    def submit_all_urls_to_indexnow(self, request, queryset):
        try:
            site = Site.objects.get_current()
            sitemap_url = f"/sitemap.xml"
            success = submit_to_indexnow([sitemap_url])
            
            for obj in queryset:
                obj.last_indexnow_submission = timezone.now()
                obj.save()
            
            if success:
                self.message_user(request, "Successfully submitted URLs to IndexNow!", messages.SUCCESS)
            else:
                self.message_user(request, "IndexNow submission completed with some errors. Check logs.", messages.WARNING)
        except Exception as e:
            self.message_user(request, f"Error submitting to IndexNow: {e}", messages.ERROR)


@admin.register(IndexNowSubmission)
class IndexNowSubmissionAdmin(admin.ModelAdmin):
    list_display = ['status_icon', 'url', 'submitted_at', 'response_code']
    list_filter = ['success', 'submitted_at']
    search_fields = ['url', 'error_message']
    readonly_fields = ['url', 'submitted_at', 'success', 'response_code', 'error_message']
    ordering = ['-submitted_at']
    
    def has_add_permission(self, request):
        return False
    
    def status_icon(self, obj):
        if obj.success:
            return format_html('<span style="color: green;">✓ Success</span>')
        return format_html('<span style="color: red;">✗ Failed</span>')
    status_icon.short_description = 'Status'
    
    actions = ['retry_failed_submissions']
    
    @admin.action(description='Retry failed IndexNow submissions')
    def retry_failed_submissions(self, request, queryset):
        failed = queryset.filter(success=False)
        urls = [obj.url for obj in failed]
        if urls:
            success = submit_to_indexnow(urls)
            if success:
                self.message_user(request, f"Retried {len(urls)} failed submissions", messages.SUCCESS)
            else:
                self.message_user(request, "Retry completed with errors", messages.WARNING)
        else:
            self.message_user(request, "No failed submissions to retry", messages.INFO)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'category', 'subject', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['subject', 'description', 'email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Ticket Information', {
            'fields': ('user', 'email', 'category', 'subject', 'description')
        }),
        ('Status', {
            'fields': ('status', 'resolved_at')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

