from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Product views
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart and Checkout
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Order Management
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order-history/', views.order_history, name='order_history'),
    
    # Payment
    path('payment/', views.payment, name='payment'),
    
    # Authentication
    path('register/', views.register, name='register'),
]
