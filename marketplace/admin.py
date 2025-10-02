from django.contrib import admin
from .models import Category, Service, ServiceImage, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 3
    fields = ('image', 'order')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'artisan', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'artisan__username')
    inlines = [ServiceImageInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # --- Removed 'is_confirmed' from list_display and list_filter ---
    list_display = ('service', 'customer_name', 'customer_email', 'requested_at')
    list_filter = ('requested_at',)
    search_fields = ('customer_name', 'customer_email', 'service__title')