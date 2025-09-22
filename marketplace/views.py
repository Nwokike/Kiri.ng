from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Service, Booking
from .forms import ServiceForm, BookingForm
from django.db.models import Count
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class ServiceListView(generic.ListView):
    model = Service
    template_name = 'marketplace/service_list.html'
    context_object_name = 'services'
    queryset = Service.objects.filter(artisan__isnull=False).order_by('-id')

class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'marketplace/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookingForm()
        # ... recommendation logic remains the same ...
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = self.object
            if request.user.is_authenticated:
                booking.customer_user = request.user
            booking.save()

            # --- THIS IS THE FIX: Simplified and robust email sending ---
            try:
                artisan_user = self.object.artisan
                context = {
                    'artisan_name': artisan_user.username,
                    'service_title': self.object.title,
                    'booking': booking,
                }
                html_message = render_to_string('marketplace/booking_notification_email.html', context)
                plain_message = strip_tags(html_message)
                
                print("--- SENDING BOOKING EMAIL ---") # For debugging
                print(f"To: {artisan_user.email}")

                send_mail(
                    f'New Booking Request for "{self.object.title}"',
                    plain_message,
                    'noreply@kiri.ng',
                    [artisan_user.email],
                    html_message=html_message,
                )
            except Exception as e:
                print(f"ERROR SENDING BOOKING EMAIL: {e}")

            messages.success(request, _("Your booking request has been sent!"))
            return redirect('marketplace:service-detail', pk=self.object.pk)
        else:
            messages.error(request, _("There was an error in your booking form."))
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

# ... other marketplace views remain the same ...
class ArtisanDashboardView(LoginRequiredMixin, generic.ListView):
    # ...
    model = Service
    template_name = 'marketplace/artisan_dashboard.html'
    context_object_name = 'services'
    def get_queryset(self): return Service.objects.filter(artisan=self.request.user).order_by('-id')

class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    # ...
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')
    def form_valid(self, form):
        form.instance.artisan = self.request.user
        messages.success(self.request, _("Your new service has been created."))
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, generic.UpdateView):
    # ...
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')
    def get_queryset(self): return Service.objects.filter(artisan=self.request.user)
    def form_valid(self, form):
        messages.success(self.request, _("Your service has been updated."))
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    # ...
    model = Service
    template_name = 'marketplace/service_confirm_delete.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')
    def get_queryset(self): return Service.objects.filter(artisan=self.request.user)
    def form_valid(self, form):
        messages.success(self.request, _("The service has been successfully deleted."))
        return super().form_valid(form)