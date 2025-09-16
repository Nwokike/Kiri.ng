from django.contrib import admin

# Register your models here.
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'verified')
    list_filter = ('role', 'verified')
    search_fields = ('user__username',)
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_as_verified.short_description = "Mark selected profiles as verified"