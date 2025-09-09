from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart'),
    path('promotions/', views.promotions, name='promotions'),
    path('flash-sale/', views.flash_sale, name='flash_sale'),
    path('news/', views.news, name='news'),
    path('brands/', views.brands, name='brands'),
    path('stores/', views.stores, name='stores'),
    path('order-lookup/', views.order_lookup, name='order_lookup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('policy/', views.policy, name='policy'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('products/orders/', views.user_orders, name='user_orders'),
]