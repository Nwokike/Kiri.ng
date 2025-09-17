from django.contrib import admin

# Register your models here.
from .models import Booking, Review

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'buyer', 'booking_date', 'status')
    list_filter = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'reviewer', 'rating', 'created_at')