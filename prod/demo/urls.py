from demo import views
from django.urls import path
from django.contrib.auth import views as auth_views
from demo.views import *

urlpatterns = [
    # path('login/', views.login),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('', catalog, name='catalog'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('product', product, name='product'),

    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('orders', orders, name='orders'),
    path('delete_order/<pk>', delete_order, name='delete_order'),
    path('detail/<pk>', ProductDetail.as_view(), name='product_detail'),
    path('to_cart/<pk>', to_cart, name='to_cart'),
    path('remove_from_cart/<pk>', remove_from_cart, name='remove_from_cart'),
]
