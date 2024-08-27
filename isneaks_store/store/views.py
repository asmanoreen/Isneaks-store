from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

def home(request):
    return render(request, 'store/home.html')

def about_us(request):
    return render(request, 'store/about_us.html')

def shop(request):
    return render(request, 'store/shop.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'store/login.html'
    success_url = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')