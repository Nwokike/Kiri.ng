from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from core.models import Service

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('completed', 'Completed'),
        ('cancelled', _('Cancelled')),
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Service"))
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Buyer"))
    booking_date = models.DateTimeField(verbose_name=_("Booking Date"))
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(_("Notes for the Entrepreneur"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.service.title} by {self.buyer.username}"

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Service"))
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Reviewer"))
    rating = models.PositiveIntegerField(_("Rating"), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.service.title} by {self.reviewer.username}"