from django.contrib import admin
from .models import LearningPathway, PathwayModule, ModuleStep, Badge, UserBadge, Comment

@admin.register(LearningPathway)
class LearningPathwayAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'created_at')
    search_fields = ('goal', 'user__username')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pathway', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('body', 'author__username', 'pathway__goal')

admin.site.register(PathwayModule)
admin.site.register(ModuleStep)