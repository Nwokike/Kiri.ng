from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Service, Category
from .forms import ServiceForm, BookingForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class ServiceListView(generic.ListView):
    model = Service
    template_name = 'marketplace/service_list.html'
    context_object_name = 'services'
    paginate_by = 10

class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'marketplace/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_form'] = BookingForm()
        return context

    def post(self, request, *args, **kwargs):
        service = self.get_object()
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.save()
            
            try:
                artisan_user = service.entrepreneur
                context = {
                    'artisan_name': artisan_user.username,
                    'service_title': service.title,
                    'booking': booking,
                }
                html_message = render_to_string('marketplace/booking_notification_email.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    f'New Booking Request for "{service.title}"',
                    plain_message,
                    'noreply@kiri.ng',
                    [artisan_user.email],
                    html_message=html_message,
                )
                print(f"Booking notification email sent to {artisan_user.email}")
            except Exception as e:
                print(f"Error sending email: {e}")


            messages.success(request, _("Your booking request has been sent! The artisan will contact you shortly."))
            return redirect('marketplace:service-detail', pk=service.pk)
        
        context = self.get_context_data()
        context['booking_form'] = form
        return self.render_to_response(context)

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:service-list')

    def test_func(self):
        return self.request.user.profile.is_verified_artisan

    def handle_no_permission(self):
        messages.error(self.request, _("You must be a verified artisan to add a new service."))
        return redirect('users:profile-detail')

    def form_valid(self, form):
        form.instance.entrepreneur = self.request.user
        messages.success(self.request, _("Your service has been created successfully!"))
        return super().form_valid(form)
    
class ArtisanDashboardView(LoginRequiredMixin, generic.ListView):
    model = Service
    template_name = 'marketplace/artisan_dashboard.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(entrepreneur=self.request.user).order_by('-created_at')


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def test_func(self):
        service = self.get_object()
        return self.request.user == service.entrepreneur

    def form_valid(self, form):
        messages.success(self.request, _("Your service has been updated successfully!"))
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Service
    template_name = 'marketplace/service_confirm_delete.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def test_func(self):
        service = self.get_object()
        return self.request.user == service.entrepreneur
    
    def form_valid(self, form):
        messages.success(self.request, _("Your service has been deleted successfully."))
        return super().form_valid(form)