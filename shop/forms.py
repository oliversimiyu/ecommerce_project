from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, ProductReview, Product, Cart, CartItem, Order, OrderItem

class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile
    """
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'phone_number', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class ProductReviewForm(forms.ModelForm):
    """
    Form for submitting product reviews
    """
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
        }

class ProductFilterForm(forms.Form):
    """
    Form for filtering products
    """
    category = forms.ModelChoiceField(
        queryset=Product.objects.values_list('category', flat=True).distinct(), 
        required=False
    )
    brand = forms.CharField(max_length=200, required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    is_featured = forms.BooleanField(required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Product.objects.values_list('tags', flat=True).distinct(), 
        required=False
    )

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user information
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, 
        max_value=10, 
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'style': 'width: 80px;'
        })
    )
    product_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product_id = self.cleaned_data['product_id']
        
        try:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                raise forms.ValidationError(f"Sorry, only {product.stock} items available.")
        except Product.DoesNotExist:
            raise forms.ValidationError("Invalid product.")
        
        return quantity

class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe')
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES, 
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = Order
        fields = [
            'shipping_name', 
            'shipping_address', 
            'shipping_city', 
            'shipping_postal_code', 
            'shipping_country'
        ]
        widgets = {
            'shipping_name': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'shipping_city': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'shipping_country': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation can be added here
        return cleaned_data
