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
    # path('cart/', views.cart, name='cart'),
]