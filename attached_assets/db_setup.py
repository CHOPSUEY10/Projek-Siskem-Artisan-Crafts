#!/usr/bin/env python
import os
import sys
import django
from django.core.files.images import ImageFile
from django.utils.text import slugify
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings.development')
django.setup()

from core.models import Item, CATEGORY_CHOICES, LABEL_CHOICES

# Sample artisan craft products
PRODUCTS = [
    # Pottery Items
    {
        'title': 'Handmade Ceramic Mug',
        'price': 24.99,
        'discount_price': 19.99,
        'category': 'PT',
        'label': 'P',
        'description': 'Handcrafted ceramic mug made with traditional techniques. Each piece is unique with a beautiful glazed finish. Perfect for your morning coffee or tea.',
        'additional_info': 'Microwave and dishwasher safe. Food-safe glazes used. Approximate size: 3.5" height, 3" diameter.',
        'artisan_name': 'Maria Rodriguez',
        'artisan_location': 'Mexico',
        'materials': 'Locally sourced clay, food-safe glazes',
        'featured': True
    },
    {
        'title': 'Decorative Clay Vase',
        'price': 59.99,
        'discount_price': None,
        'category': 'PT',
        'label': 'S',
        'description': 'Elegant hand-thrown vase with intricate hand-painted designs. This beautiful piece adds a touch of artisanal charm to any space.',
        'additional_info': 'For decorative use only. Not water-tight. Height: 10", Width: 6".',
        'artisan_name': 'Carlos Mendez',
        'artisan_location': 'Colombia',
        'materials': 'Terracotta clay, mineral-based paints',
        'featured': True
    },
    
    # Jewelry Items
    {
        'title': 'Beaded Statement Necklace',
        'price': 45.99,
        'discount_price': 38.99,
        'category': 'JW',
        'label': 'D',
        'description': 'Handcrafted statement necklace featuring colorful glass beads and traditional patterns. Each piece is carefully assembled by skilled artisans.',
        'additional_info': 'Length: 18" with 2" extender. Clasp: Lobster claw. Avoid contact with water and perfumes.',
        'artisan_name': 'Amara Okafor',
        'artisan_location': 'Kenya',
        'materials': 'Glass beads, waxed cotton cord, brass findings',
        'featured': False
    },
    {
        'title': 'Silver Filigree Earrings',
        'price': 35.00,
        'discount_price': None,
        'category': 'JW',
        'label': 'P',
        'description': 'Delicate silver filigree earrings handcrafted using traditional techniques passed down through generations. Light and comfortable to wear.',
        'additional_info': 'Length: 1.5". Posts are sterling silver. Store in a dry place away from humidity.',
        'artisan_name': 'Lucia Torres',
        'artisan_location': 'Peru',
        'materials': 'Sterling silver',
        'featured': True
    },
    
    # Textiles
    {
        'title': 'Hand-woven Wool Tapestry',
        'price': 129.99,
        'discount_price': 99.99,
        'category': 'TX',
        'label': 'S',
        'description': 'Beautiful wall hanging tapestry, hand-woven on a traditional loom using natural wool yarns. Features geometric patterns inspired by ancient traditions.',
        'additional_info': 'Size: 24" x 36". Comes with wooden hanging rod. Spot clean only with cold water if necessary.',
        'artisan_name': 'Isabel Quispe',
        'artisan_location': 'Bolivia',
        'materials': 'Natural sheep wool, vegetable dyes',
        'featured': True
    },
    {
        'title': 'Block Printed Cotton Table Runner',
        'price': 38.50,
        'discount_price': None,
        'category': 'TX',
        'label': 'P',
        'description': 'Hand block-printed table runner made with 100% cotton. Each piece is printed by hand using carved wooden blocks and natural dyes.',
        'additional_info': 'Size: 14" x 72". Machine wash cold, tumble dry low. Ironing may be required after washing.',
        'artisan_name': 'Raj Sharma',
        'artisan_location': 'India',
        'materials': 'Organic cotton, natural dyes',
        'featured': False
    },
    
    # Woodwork
    {
        'title': 'Hand-carved Wooden Bowl',
        'price': 49.99,
        'discount_price': None,
        'category': 'WD',
        'label': 'P',
        'description': 'Beautiful wooden bowl hand-carved from a single piece of sustainable hardwood. Each bowl showcases the natural grain and unique character of the wood.',
        'additional_info': 'Diameter: 8". Hand wash only with mild soap, dry immediately. Periodically treat with food-safe mineral oil.',
        'artisan_name': 'Thomas Okello',
        'artisan_location': 'Uganda',
        'materials': 'Sustainable olive wood',
        'featured': False
    },
    {
        'title': 'Decorative Wooden Box with Inlay',
        'price': 85.00,
        'discount_price': 72.50,
        'category': 'WD',
        'label': 'S',
        'description': 'Exquisite wooden box with intricate inlay work. Handcrafted by skilled woodworkers using traditional techniques. Perfect for storing small treasures.',
        'additional_info': 'Size: 6" x 4" x 2.5". Lined with soft velvet. Wipe clean with a dry cloth.',
        'artisan_name': 'Ahmed Hassan',
        'artisan_location': 'Morocco',
        'materials': 'Walnut wood, mother of pearl inlay',
        'featured': True
    },
    
    # Home Decor
    {
        'title': 'Hand-painted Ceramic Planter',
        'price': 32.99,
        'discount_price': 27.99,
        'category': 'HM',
        'label': 'P',
        'description': 'Colorful hand-painted ceramic planter featuring traditional patterns. Each piece is uniquely painted by skilled artisans.',
        'additional_info': 'Size: 6" diameter, 5" height. Includes drainage hole. Indoor use recommended.',
        'artisan_name': 'Fatima El Mansouri',
        'artisan_location': 'Morocco',
        'materials': 'Ceramic, lead-free paints',
        'featured': False
    },
    {
        'title': 'Macrame Wall Hanging',
        'price': 65.00,
        'discount_price': None,
        'category': 'HM',
        'label': 'S',
        'description': 'Intricate macrame wall hanging handcrafted with natural cotton rope. Each piece is meticulously knotted to create a beautiful bohemian accent for your home.',
        'additional_info': 'Size: 24" wide x 36" long. Hangs from a wooden dowel. Spot clean only if necessary.',
        'artisan_name': 'Sofia Mendoza',
        'artisan_location': 'Mexico',
        'materials': 'Unbleached cotton rope, reclaimed wooden dowel',
        'featured': True
    },
    
    # Sculptures
    {
        'title': 'Soapstone Animal Sculpture',
        'price': 42.99,
        'discount_price': None,
        'category': 'SC',
        'label': 'P',
        'description': 'Hand-carved soapstone sculpture of a elephant. Each piece is sculpted by skilled artisans who have practiced this craft for generations.',
        'additional_info': 'Size: approximately 4" high. Due to the handmade nature, each piece varies slightly in color and pattern.',
        'artisan_name': 'Joseph Mutua',
        'artisan_location': 'Kenya',
        'materials': 'Natural soapstone',
        'featured': False
    },
    {
        'title': 'Bronze Lost-Wax Cast Figurine',
        'price': 120.00,
        'discount_price': 99.99,
        'category': 'SC',
        'label': 'D',
        'description': 'Beautiful bronze figurine created using the traditional lost-wax casting method. This ancient technique produces detailed sculptures with rich character.',
        'additional_info': 'Height: 7". Patina will naturally develop over time, adding to the unique character of the piece.',
        'artisan_name': 'Kofi Amoah',
        'artisan_location': 'Ghana',
        'materials': 'Recycled bronze',
        'featured': True
    },
]

def create_sample_products():
    print("Creating sample artisan craft products...")
    
    for product in PRODUCTS:
        # Generate a slug from the title
        slug = slugify(product['title'])
        
        # Check if product with this slug already exists
        if Item.objects.filter(slug=slug).exists():
            print(f"Product '{product['title']}' already exists. Skipping.")
            continue
        
        # Create the product
        new_product = Item(
            title=product['title'],
            price=product['price'],
            discount_price=product['discount_price'],
            category=product['category'],
            label=product['label'],
            slug=slug,
            description=product['description'],
            additional_info=product['additional_info'],
            artisan_name=product['artisan_name'],
            artisan_location=product['artisan_location'],
            materials=product['materials'],
            featured=product['featured']
        )
        
        # Save the product
        new_product.save()
        print(f"Created product: {product['title']}")

if __name__ == '__main__':
    print("Starting product setup script...")
    create_sample_products()
    print("Setup completed successfully!")
