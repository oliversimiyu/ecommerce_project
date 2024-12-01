from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.models import Category, Product, Tag
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Add sample products to the database'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Clothing', 'slug': 'clothing'},
            {'name': 'Home & Kitchen', 'slug': 'home-kitchen'},
            {'name': 'Books', 'slug': 'books'},
            {'name': 'Sports & Outdoors', 'slug': 'sports-outdoors'}
        ]

        created_categories = []
        for cat_data in categories:
            category, created = Category.objects.get_or_create(**cat_data)
            created_categories.append(category)

        # Create tags with explicit slug generation
        tag_names = ['bestseller', 'new', 'sale', 'trending', 'premium']

        created_tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=tag_name, 
                defaults={'slug': slugify(tag_name)}
            )
            created_tags.append(tag)

        # Sample product data
        products_data = [
            {
                'name': 'Wireless Noise Cancelling Headphones',
                'description': 'Premium over-ear headphones with advanced noise cancellation technology.',
                'category': created_categories[0],
                'price': 249.99,
                'brand': 'SoundWave',
                'is_featured': True,
                'tags': [created_tags[0], created_tags[1]],
                'image_path': 'shop/sample_images/headphones.jpg',
                'stock': 50
            },
            {
                'name': 'Smart Fitness Tracker',
                'description': 'Advanced fitness tracker with heart rate monitoring and GPS tracking.',
                'category': created_categories[4],
                'price': 129.99,
                'brand': 'FitTech',
                'is_featured': True,
                'tags': [created_tags[2], created_tags[4]],
                'image_path': 'shop/sample_images/fitness_tracker.jpg',
                'stock': 75
            },
            {
                'name': 'Leather Messenger Bag',
                'description': 'Stylish and durable leather messenger bag for professionals.',
                'category': created_categories[1],
                'price': 189.50,
                'brand': 'Urban Craft',
                'is_featured': False,
                'tags': [created_tags[3]],
                'image_path': 'shop/sample_images/messenger_bag.jpg',
                'stock': 30
            },
            {
                'name': 'Bestselling Sci-Fi Novel Collection',
                'description': 'Curated collection of top-rated science fiction novels from contemporary authors.',
                'category': created_categories[3],
                'price': 49.99,
                'brand': 'Nebula Press',
                'is_featured': True,
                'tags': [created_tags[0], created_tags[1]],
                'image_path': 'shop/sample_images/sci-fi_books.jpg',
                'stock': 100
            },
            {
                'name': 'Smart Home Assistant',
                'description': 'Voice-activated smart home device with AI capabilities and home automation features.',
                'category': created_categories[2],
                'price': 149.99,
                'brand': 'HomeGenius',
                'is_featured': True,
                'tags': [created_tags[1], created_tags[4]],
                'image_path': 'shop/sample_images/smart_home_assistant.jpg',
                'stock': 60
            }
        ]

        # Create products
        for product_info in products_data:
            # Prepare image
            try:
                with open(product_info['image_path'], 'rb') as img_file:
                    image = SimpleUploadedFile(
                        name=product_info['image_path'].split('/')[-1], 
                        content=img_file.read(), 
                        content_type='image/jpeg'
                    )
            except FileNotFoundError:
                # Create a placeholder image if the file doesn't exist
                image = SimpleUploadedFile(
                    name='placeholder.jpg', 
                    content=b'', 
                    content_type='image/jpeg'
                )

            # Create product
            product, created = Product.objects.get_or_create(
                name=product_info['name'],
                defaults={
                    'slug': slugify(product_info['name']),
                    'description': product_info['description'],
                    'category': product_info['category'],
                    'price': product_info['price'],
                    'brand': product_info['brand'],
                    'is_featured': product_info['is_featured'],
                    'image': image,
                    'available': True,
                    'stock': product_info['stock']
                }
            )

            # Add tags
            product.tags.set(product_info['tags'])

        self.stdout.write(self.style.SUCCESS('Successfully added sample products'))
