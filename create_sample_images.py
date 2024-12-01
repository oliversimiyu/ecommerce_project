import os
from PIL import Image, ImageDraw, ImageFont

# Ensure sample images directory exists
os.makedirs('shop/sample_images', exist_ok=True)

# List of product names
products = [
    'Headphones', 
    'Fitness Tracker', 
    'Messenger Bag', 
    'Sci-Fi Books', 
    'Smart Home Assistant'
]

# Create sample images
for product in products:
    # Create a new white image
    img = Image.new('RGB', (800, 600), color='white')
    
    # Create a drawing context
    d = ImageDraw.Draw(img)
    
    # Use a default font (you might want to adjust path for different systems)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        # Fallback to default font if arial.ttf is not found
        font = ImageFont.load_default()
    
    # Draw product name
    d.text((50,250), product, fill=(0,0,0), font=font)
    
    # Save the image
    filename = f'shop/sample_images/{product.lower().replace(" ", "_")}.jpg'
    img.save(filename)
    print(f"Created {filename}")
