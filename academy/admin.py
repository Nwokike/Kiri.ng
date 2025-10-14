from django.contrib import admin
from .models import LearningPathway, PathwayModule, ModuleStep, Badge, UserBadge, Comment, ModuleVideo, ModuleQuestion, ModuleQuiz

class PathwayModuleInline(admin.TabularInline):
    model = PathwayModule
    extra = 0
    readonly_fields = ('title', 'order', 'is_completed')
    can_delete = False
    ordering = ('order',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'body', 'created_at')

class ModuleVideoInline(admin.TabularInline):
    model = ModuleVideo
    extra = 0
    ordering = ('order',)

class ModuleQuestionInline(admin.TabularInline):
    model = ModuleQuestion
    extra = 0
    readonly_fields = ('user', 'question_text', 'created_at')

@admin.register(LearningPathway)
class LearningPathwayAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'created_at')
    search_fields = ('goal', 'user__username')
    inlines = [PathwayModuleInline, CommentInline]

@admin.register(PathwayModule)
class PathwayModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pathway', 'order', 'is_completed')
    list_filter = ('is_completed', 'content_generated')
    search_fields = ('title', 'pathway__goal')
    inlines = [ModuleVideoInline, ModuleQuestionInline]

@admin.register(ModuleVideo)
class ModuleVideoAdmin(admin.ModelAdmin):
    list_display = ('module', 'title', 'order')
    search_fields = ('title', 'module__title')

@admin.register(ModuleQuestion)
class ModuleQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'question_text', 'answered', 'created_at')
    list_filter = ('answered', 'created_at')
    search_fields = ('question_text', 'user__username', 'module__title')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    list_filter = ('badge',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pathway', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('body', 'author__username', 'pathway__goal')

@admin.register(ModuleQuiz)
class ModuleQuizAdmin(admin.ModelAdmin):
    list_display = ('module', 'question', 'correct_answer')
    search_fields = ('question', 'module__title')

admin.site.register(ModuleStep)