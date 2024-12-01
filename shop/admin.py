from django.contrib import admin
from .models import Category, Product, UserProfile, ProductReview, Tag, Cart, CartItem, Order, OrderItem

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available']
    list_filter = ['category', 'available', 'created']
    search_fields = ['name', 'description']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_name']
    inlines = [OrderItemInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ['product', 'quantity']
    can_delete = True
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile)
admin.site.register(ProductReview)
admin.site.register(Tag)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CartItem)
admin.site.register(OrderItem)
