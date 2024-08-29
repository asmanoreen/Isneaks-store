from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .models import Product

def home(request):
    # Fetch all products with their associated images
    products = Product.objects.prefetch_related('productimage_set').all()
    for product in products:
        product.image_url = product.productimage_set.first().image if product.productimage_set.first().image else ''
    return render(request, 'store/home.html', {'products': products})

def about_us(request):
    return render(request, 'store/about_us.html')

def shop(request):
    # Fetch all products with their associated images
    products = Product.objects.prefetch_related('productimage_set').all()
    for product in products:
        product.image_url = product.productimage_set.first().image if product.productimage_set.first().image else ''
    return render(request, 'store/shop.html', {'products': products})

def contact_us(request):
    return render(request, 'store/contact_us.html')

def product_detail(request, pk):
    products = Product.objects.prefetch_related('productimage_set').all()
    for product in products:
        product.image_url = product.productimage_set.first().image if product.productimage_set.first().image else ''
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product, 'products': products})

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'store/login.html'
    success_url = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
