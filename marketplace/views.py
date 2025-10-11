from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Service, Booking, Category, ServiceImage
from .forms import ServiceForm, BookingForm
from django.db.models import Count, Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from notifications.models import Notification   # ✅ Added import


class ServiceListView(generic.ListView):
    model = Service
    template_name = 'marketplace/service_list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        queryset = Service.objects.filter(artisan__isnull=False).select_related('artisan', 'category')
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        else:
            queryset = queryset.order_by('-created_at')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.kwargs.get('category_slug')
        return context


class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'marketplace/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookingForm()

        # ML-based recommender logic
        service = self.get_object()
        all_services = Service.objects.filter(category=service.category).exclude(pk=service.pk)

        if all_services.count() > 1:
            try:
                descriptions = [s.description for s in all_services]
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(descriptions)
                service_tfidf = vectorizer.transform([service.description])
                cosine_similarities = cosine_similarity(service_tfidf, tfidf_matrix).flatten()
        
                related_indices = cosine_similarities.argsort()[-2:][::-1]
                recommended_pks = [all_services[i].pk for i in related_indices if cosine_similarities[i] > 0.1]
                context['recommended_services'] = Service.objects.filter(pk__in=recommended_pks)
            except Exception:
                # Fallback to random services if ML fails
                context['recommended_services'] = all_services.order_by('?')[:2]
        elif all_services.exists():
            context['recommended_services'] = all_services.order_by('?')[:2]

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = self.object

            if request.user.is_authenticated:
                booking.customer_user = request.user
                booking.customer_name = request.user.get_full_name()
                booking.customer_email = request.user.email

            booking.save()

            # ✅ Create a notification for the artisan
            Notification.objects.create(
                recipient=self.object.artisan,
                message=_(f"You have a new booking request for '{self.object.title}' from {booking.customer_name}."),
                link=reverse('marketplace:service-detail', kwargs={'pk': self.object.pk})
            )

            # --- existing email sending logic ---
            subject = _("New Booking Request")
            context = {
                "booking": booking,
                "artisan_name": self.object.artisan.get_full_name() or self.object.artisan.username,
                "service_title": self.object.title
            }
            html_message = render_to_string("marketplace/booking_notification_email.html", context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject,
                plain_message,
                None,  # from email (uses DEFAULT_FROM_EMAIL)
                [self.object.artisan.email],
                html_message=html_message,
            )

            messages.success(request, _("Your booking request has been sent! The artisan will contact you shortly."))
            return redirect('marketplace:service-detail', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ArtisanDashboardView(LoginRequiredMixin, generic.ListView):
    model = Service
    template_name = 'marketplace/artisan_dashboard.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(artisan=self.request.user).order_by('-id')


class ServiceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def form_valid(self, form):
        form.instance.artisan = self.request.user
        response = super().form_valid(form)
        
        additional_images = self.request.FILES.getlist('additional_images')
        for idx, image in enumerate(additional_images):
            ServiceImage.objects.create(
                service=self.object,
                image=image,
                order=idx
            )
        
        messages.success(self.request, _("Your new service has been created."))
        return response


class ServiceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'marketplace/service_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def get_queryset(self):
        return Service.objects.filter(artisan=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        additional_images = self.request.FILES.getlist('additional_images')
        for idx, image in enumerate(additional_images):
            ServiceImage.objects.create(
                service=self.object,
                image=image,
                order=idx
            )
        
        messages.success(self.request, _("Your service has been updated."))
        return response


class ServiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Service
    template_name = 'marketplace/service_confirm_delete.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def get_queryset(self):
        return Service.objects.filter(artisan=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, _("The service has been successfully deleted."))
        return super().form_valid(form)
