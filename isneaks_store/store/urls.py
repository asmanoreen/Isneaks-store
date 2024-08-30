from django.urls import path
from .views import CustomLoginView, CustomLogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about_us, name='about-us'),
    path('shop/', views.shop, name='shop'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]