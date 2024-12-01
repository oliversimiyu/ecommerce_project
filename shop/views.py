from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Category, Product, Cart, CartItem, Order, OrderItem, UserProfile, ProductReview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserProfileForm, ProductReviewForm, ProductFilterForm, UserUpdateForm, AddToCartForm, CheckoutForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    filter_form = ProductFilterForm(request.GET)
    
    if filter_form.is_valid():
        category = filter_form.cleaned_data.get('category')
        brand = filter_form.cleaned_data.get('brand')
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        is_featured = filter_form.cleaned_data.get('is_featured')
        tags = filter_form.cleaned_data.get('tags')
        
        if category:
            products = products.filter(category=category)
        if brand:
            products = products.filter(brand__icontains=brand)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        if is_featured:
            products = products.filter(is_featured=True)
        if tags:
            products = products.filter(tags__in=tags)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'filter_form': filter_form
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            # Check if user has already reviewed this product
            existing_review = ProductReview.objects.filter(
                product=product, 
                user=request.user
            ).exists()
            
            if not existing_review:
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted!')
            else:
                messages.warning(request, 'You have already reviewed this product.')
            
            return redirect('shop:product_detail', slug=slug)
    else:
        review_form = ProductReviewForm()
    
    # Get product reviews
    reviews = ProductReview.objects.filter(product=product)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'average_rating': average_rating
    })

@login_required
def cart_detail(request):
    """
    Display the user's cart details
    """
    # Get or create the cart for the current user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Fetch all cart items for this cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate total price
    total_price = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart': {
            'items': cart_items,
            'total_price': total_price,
            'count': cart_items.count()
        }
    }
    
    return render(request, 'shop/cart_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the cart. If the product is already in the cart, 
    increase its quantity.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Ensure user is logged in
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to add items to your cart.")
        return redirect('login')

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': 1}
    )

    # If the item already exists, increment quantity
    if not item_created:
        # Check if adding would exceed available stock
        if cart_item.quantity + 1 > product.stock:
            messages.warning(request, f"Sorry, only {product.stock} items available.")
        else:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{product.name} quantity updated in cart.")
    else:
        messages.success(request, f"{product.name} added to cart.")

    return redirect('shop:product_list')

@login_required
def remove_from_cart(request, cart_item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    
    # Restore product stock
    product = cart_item.product
    product.stock += cart_item.quantity
    product.save()
    
    cart_item.delete()
    messages.success(request, f'{cart_item.product.name} removed from cart.')
    return redirect('shop:cart_detail')

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart.')
    return redirect('shop:cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('shop:cart_detail')

@login_required
def cart_update(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    else:
        CartItem.objects.filter(cart=cart, product=product).delete()
    
    return redirect('shop:cart_detail')

@login_required
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = order.order_items.select_related('product')
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'shop/order_detail.html', context)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('shop:order_history')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'shop/order_history.html', context)

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to complete your purchase.")
        return redirect('shop:login')

    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.select_related('product')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create Order
            order = Order.objects.create(
                user=request.user,
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_address=form.cleaned_data['shipping_address'],
                shipping_city=form.cleaned_data['shipping_city'],
                shipping_postal_code=form.cleaned_data['shipping_postal_code'],
                shipping_country=form.cleaned_data['shipping_country'],
                total_price=sum(item.product.price * item.quantity for item in cart_items)
            )

            # Create OrderItems and update stock
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                # Update product stock
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()

            # Clear the cart
            cart_items.delete()

            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect('shop:order_detail', order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'shipping_name': request.user.get_full_name(),
        })

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': sum(item.product.price * item.quantity for item in cart_items)
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def payment(request):
    # Create Stripe checkout session
    success_url = request.build_absolute_uri('/payment/success/')
    cancel_url = request.build_absolute_uri('/payment/cancel/')
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Order Payment',
                },
                'unit_amount': int(request.user.order_set.latest('created').total_cost * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    
    return render(request, 'shop/payment.html', {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def payment_success(request):
    order = request.user.order_set.latest('created')
    order.status = 'processing'
    order.save()
    messages.success(request, 'Payment successful! Your order is being processed.')
    return redirect('shop:order_detail', order_id=order.id)

@login_required
def payment_cancel(request):
    messages.error(request, 'Payment cancelled. Please try again.')
    return redirect('shop:checkout')

@login_required
def order_create(request):
    cart = Cart.objects.get(user=request.user)
    
    # Create the order
    order = Order.objects.create(
        user=request.user,
        status='pending'
    )
    
    # Create order items from cart
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )
    
    # Clear the cart
    cart.items.all().delete()
    
    messages.success(request, 'Order created successfully!')
    return redirect('shop:order_tracking', order_id=order.id)

@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_tracking.html', {'order': order})

@login_required
def profile_update(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('shop:user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    return render(request, 'shop/profile_update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            # Check if user has already reviewed this product
            existing_review = ProductReview.objects.filter(
                product=product, 
                user=request.user
            ).exists()
            
            if not existing_review:
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted!')
            else:
                messages.warning(request, 'You have already reviewed this product.')
            
            return redirect('shop:product_detail', slug=product.slug)
    
    return redirect('shop:product_detail', slug=product.slug)

@login_required
def user_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Get recent orders
    orders = Order.objects.filter(user=request.user).order_by('-created')[:5]
    
    # Get recent reviews
    reviews = ProductReview.objects.filter(user=request.user).order_by('-created_at')[:3]
    
    return render(request, 'shop/user_profile.html', {
        'profile': profile,
        'orders': orders,
        'reviews': reviews
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def home(request):
    """
    Home page view showing only featured products
    """
    featured_products = Product.objects.filter(is_featured=True).select_related('category')
    
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'shop/home.html', context)
