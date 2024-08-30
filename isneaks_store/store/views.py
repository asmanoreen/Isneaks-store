from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .models import Product, Cart, CartItem

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'store/login.html'
    success_url = reverse_lazy('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

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


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.select_related('product').prefetch_related('product__productimage_set').all()
    return render(request, 'store/cart.html', {'cart': cart, 'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    cart.add_item(product, quantity)
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.cart.remove_item(cart_item)
    return redirect('cart')