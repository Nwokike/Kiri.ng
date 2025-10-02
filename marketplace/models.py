from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Service(models.Model):
    artisan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Price in NGN"))
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_all_images(self):
        """Return all images for this service, including the primary image and additional images"""
        images = []
        if self.image:
            images.append(self.image.url)
        images.extend([img.image.url for img in self.additional_images.all()])
        return images

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='service_images/')
    order = models.PositiveIntegerField(default=0, help_text=_("Display order"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Image for {self.service.title}"

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    # --- The 'is_confirmed' field has been removed ---

    def __str__(self):
        return f"Booking for {self.service.title} by {self.customer_name}"