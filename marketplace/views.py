from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Service, Category
from .forms import ServiceForm

class ServiceListView(generic.ListView):
    model = Service
    template_name = 'marketplace/service_list.html'
    context_object_name = 'services'
    paginate_by = 10

class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'marketplace/service_detail.html'
    context_object_name = 'service'

# --- THIS IS THE FIX ---
# We use UserPassesTestMixin to check if the user is a verified artisan.
class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:service-list')

    def test_func(self):
        # This function runs to check if the user has permission.
        # It only runs AFTER the user is successfully logged in.
        return self.request.user.profile.is_verified_artisan

    def handle_no_permission(self):
        # This message is shown if the logged-in user is NOT a verified artisan.
        messages.error(self.request, _("You must be a verified artisan to add a new service."))
        return redirect('users:profile-detail')

    def form_valid(self, form):
        form.instance.entrepreneur = self.request.user
        messages.success(self.request, _("Your service has been created successfully!"))
        return super().form_valid(form)