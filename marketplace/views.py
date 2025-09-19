from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from core.models import Service
from .models import Booking, Review
from .forms import ServiceCreateForm, BookingForm, ReviewForm
from .recommender import get_similar_services


class ServiceListView(generic.ListView):
    model = Service
    template_name = 'marketplace/service_list.html'
    context_object_name = 'services'



class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:service-list')

    def test_func(self):
        # Test if the user is a verified entrepreneur
        return self.request.user.profile.verified and self.request.user.profile.role == 'entrepreneur'

    def handle_no_permission(self):
        messages.error(self.request, _("Only verified entrepreneurs can post services. Please upload your ID for verification."))
        return redirect('users:profile')
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # We can associate the service with the logged-in user here if we add a user field to the Service model.
        # For now, we'll just save it.
        messages.success(self.request, _("Your service has been created successfully!"))
        return super().form_valid(form)

class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'marketplace/service_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current service object
        service = self.get_object()
        
        # Call our recommender function
        recommended_services = get_similar_services(service.id)

        context['booking_form'] = BookingForm()
        context['review_form'] = ReviewForm()
        context['recommended_services'] = recommended_services # <-- Add recommendations to context
        return context