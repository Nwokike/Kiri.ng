from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html', {'title': 'Kiri.ng – Empowering Artisans'})

def terms(request):
    return render(request, 'core/terms.html', {'title': 'Terms and Conditions'})

def privacy(request):
    return render(request, 'core/privacy.html', {'title': 'Privacy Policy'})