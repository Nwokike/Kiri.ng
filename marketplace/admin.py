from django.contrib import admin
from .models import Category, Service

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'entrepreneur', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'entrepreneur__username')