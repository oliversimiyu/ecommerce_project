from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify
from urllib.request import urlopen
from shop.models import Product, Category, Tag
import random
import tempfile
import os
import requests

class Command(BaseCommand):
    help = 'Populates the database with sample products'

    def download_image(self, image_url):
        """Attempt to download an image with fallback to placeholder."""
        try:
            # First try the provided URL
            if image_url:
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Use tempfile to create a temporary file
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as img_temp:
                        img_temp.write(response.content)
                        img_temp.flush()
                        return img_temp.name
            
            # If original URL fails, use a placeholder image
            placeholder_url = 'https://via.placeholder.com/500x500.png?text=Product+Image'
            response = requests.get(placeholder_url)
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as img_temp:
                img_temp.write(response.content)
                img_temp.flush()
                return img_temp.name
        
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Image download failed: {e}"))
            return None

    def handle(self, *args, **kwargs):
        # Clear existing products
        Product.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        # Create categories
        categories = [
            'Electronics', 'Clothing', 'Home & Kitchen', 
            'Books', 'Sports & Outdoors', 'Beauty & Personal Care'
        ]
        category_objs = [Category.objects.create(name=cat, slug=slugify(cat)) for cat in categories]

        # Create tags
        tags = [
            'New Arrival', 'Best Seller', 'Sale', 'Trending', 'Limited Edition'
        ]
        tag_objs = [Tag.objects.create(name=tag, slug=slugify(tag)) for tag in tags]

        # Sample products data
        products_data = [
            {
                'name': 'Wireless Noise Cancelling Headphones',
                'description': 'Premium over-ear headphones with advanced noise cancellation technology.',
                'category': 'Electronics',
                'price': 249.99,
                'stock': 50,
                'image_url': 'https://m.media-amazon.com/images/I/61-nXsCIMfL._AC_SL1500_.jpg'
            },
            {
                'name': 'Smart Fitness Tracker',
                'description': 'Advanced fitness watch with heart rate monitoring and GPS tracking.',
                'category': 'Electronics',
                'price': 129.99,
                'stock': 75,
                'image_url': 'https://m.media-amazon.com/images/I/61g2WnbR1LL._AC_SL1500_.jpg'
            },
            {
                'name': 'Organic Cotton Casual T-Shirt',
                'description': 'Soft, breathable t-shirt made from 100% organic cotton.',
                'category': 'Clothing',
                'price': 24.99,
                'stock': 100,
                'image_url': 'https://m.media-amazon.com/images/I/61ZRU9nnGTL._AC_SL1500_.jpg'
            },
            {
                'name': 'Ergonomic Office Chair',
                'description': 'Comfortable and adjustable office chair with lumbar support.',
                'category': 'Home & Kitchen',
                'price': 299.99,
                'stock': 30,
                'image_url': 'https://m.media-amazon.com/images/I/71zPriUCOEL._AC_SL1500_.jpg'
            },
            {
                'name': 'Bestselling Sci-Fi Novel Collection',
                'description': 'Set of 3 award-winning science fiction novels by top authors.',
                'category': 'Books',
                'price': 39.99,
                'stock': 60,
                'image_url': 'https://m.media-amazon.com/images/I/81Ld3VwOmOL._AC_SL1500_.jpg'
            },
            {
                'name': 'Professional Yoga Mat',
                'description': 'Extra thick, non-slip yoga mat with alignment guides.',
                'category': 'Sports & Outdoors',
                'price': 69.99,
                'stock': 45,
                'image_url': 'https://m.media-amazon.com/images/I/71grEbICRL._AC_SL1500_.jpg'
            },
            {
                'name': 'Wireless Charging Pad',
                'description': 'Fast wireless charging station compatible with multiple devices.',
                'category': 'Electronics',
                'price': 49.99,
                'stock': 80,
                'image_url': 'https://m.media-amazon.com/images/I/61-nXsCIMfL._AC_SL1500_.jpg'
            },
            {
                'name': 'Organic Skincare Set',
                'description': 'Complete skincare routine with natural and organic ingredients.',
                'category': 'Beauty & Personal Care',
                'price': 89.99,
                'stock': 40,
                'image_url': 'https://m.media-amazon.com/images/I/71grEbICRL._AC_SL1500_.jpg'
            },
            {
                'name': 'Portable Bluetooth Speaker',
                'description': 'Waterproof speaker with 360-degree sound and 12-hour battery life.',
                'category': 'Electronics',
                'price': 79.99,
                'stock': 65,
                'image_url': 'https://m.media-amazon.com/images/I/61ZRU9nnGTL._AC_SL1500_.jpg'
            },
            {
                'name': 'Leather Weekend Duffel Bag',
                'description': 'Genuine leather travel bag with multiple compartments.',
                'category': 'Clothing',
                'price': 199.99,
                'stock': 25,
                'image_url': 'https://m.media-amazon.com/images/I/81Ld3VwOmOL._AC_SL1500_.jpg'
            },
            {
                'name': 'Smart Home Security Camera',
                'description': 'HD security camera with night vision and mobile app control.',
                'category': 'Electronics',
                'price': 149.99,
                'stock': 55,
                'image_url': 'https://m.media-amazon.com/images/I/71zPriUCOEL._AC_SL1500_.jpg'
            },
            {
                'name': 'Gourmet Coffee Beans Set',
                'description': 'Collection of premium single-origin coffee beans from around the world.',
                'category': 'Home & Kitchen',
                'price': 59.99,
                'stock': 70,
                'image_url': 'https://m.media-amazon.com/images/I/61-nXsCIMfL._AC_SL1500_.jpg'
            },
            {
                'name': 'Professional Photography Book',
                'description': 'Comprehensive guide to professional photography techniques.',
                'category': 'Books',
                'price': 44.99,
                'stock': 50,
                'image_url': 'https://m.media-amazon.com/images/I/61ZRU9nnGTL._AC_SL1500_.jpg'
            },
            {
                'name': 'High-Performance Running Shoes',
                'description': 'Lightweight running shoes with advanced cushioning technology.',
                'category': 'Sports & Outdoors',
                'price': 129.99,
                'stock': 60,
                'image_url': 'https://m.media-amazon.com/images/I/81Ld3VwOmOL._AC_SL1500_.jpg'
            },
            {
                'name': 'Natural Mineral Makeup Kit',
                'description': 'Complete makeup set with natural and cruelty-free products.',
                'category': 'Beauty & Personal Care',
                'price': 79.99,
                'stock': 45,
                'image_url': 'https://m.media-amazon.com/images/I/71grEbICRL._AC_SL1500_.jpg'
            },
            {
                'name': 'Smart Robotic Vacuum Cleaner',
                'description': 'Intelligent robotic vacuum with app control and mapping technology.',
                'category': 'Home & Kitchen',
                'price': 349.99,
                'stock': 35,
                'image_url': 'https://m.media-amazon.com/images/I/71zPriUCOEL._AC_SL1500_.jpg'
            },
            {
                'name': 'Hiking Backpack',
                'description': 'Durable and comfortable 40L hiking backpack with multiple compartments.',
                'category': 'Sports & Outdoors',
                'price': 99.99,
                'stock': 40,
                'image_url': 'https://m.media-amazon.com/images/I/61-nXsCIMfL._AC_SL1500_.jpg'
            },
            {
                'name': 'Wireless Earbuds',
                'description': 'True wireless earbuds with noise cancellation and long battery life.',
                'category': 'Electronics',
                'price': 179.99,
                'stock': 65,
                'image_url': 'https://m.media-amazon.com/images/I/61ZRU9nnGTL._AC_SL1500_.jpg'
            },
            {
                'name': 'Luxury Silk Pajamas',
                'description': 'Premium silk pajama set for ultimate comfort and style.',
                'category': 'Clothing',
                'price': 149.99,
                'stock': 30,
                'image_url': 'https://m.media-amazon.com/images/I/81Ld3VwOmOL._AC_SL1500_.jpg'
            },
            {
                'name': 'Bestselling Cookbook Collection',
                'description': 'Set of 3 cookbooks featuring international cuisine and healthy recipes.',
                'category': 'Books',
                'price': 54.99,
                'stock': 55,
                'image_url': 'https://m.media-amazon.com/images/I/71grEbICRL._AC_SL1500_.jpg'
            },
            {
                'name': 'Professional Hair Styling Tools Set',
                'description': 'Complete hair styling kit with professional-grade tools.',
                'category': 'Beauty & Personal Care',
                'price': 129.99,
                'stock': 40,
                'image_url': 'https://m.media-amazon.com/images/I/61-nXsCIMfL._AC_SL1500_.jpg'
            }
        ]

        for product_info in products_data:
            # Find the category
            category = Category.objects.get(name=product_info['category'])
            
            # Download image
            img_temp_path = self.download_image(product_info.get('image_url'))

            # Create product
            product = Product.objects.create(
                name=product_info['name'],
                description=product_info['description'],
                category=category,
                price=product_info['price'],
                stock=product_info['stock'],
                available=True,
                slug=slugify(product_info['name'])
            )

            # Save image if downloaded successfully
            if img_temp_path:
                try:
                    with open(img_temp_path, 'rb') as img_file:
                        product.image.save(f"{product.id}_product.jpg", File(img_file), save=True)
                    os.unlink(img_temp_path)  # Clean up temporary file
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Could not save image for {product.name}: {e}"))

            # Add some random tags
            for _ in range(random.randint(1, 3)):
                product.tags.add(random.choice(tag_objs))

            self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated products'))
