from django.contrib import admin

# Register your models here.
from .models import LearningPathway, PathwayModule, ModuleStep, Badge, UserBadge

admin.site.register(LearningPathway)
admin.site.register(PathwayModule)
admin.site.register(ModuleStep)
admin.site.register(Badge)
admin.site.register(UserBadge)