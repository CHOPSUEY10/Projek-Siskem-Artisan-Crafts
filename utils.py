from models import Category, Item, User, Coupon
from app import db
import logging


def init_sample_data():
    """Initialize the database with sample data if it's empty"""
    
    # Check if categories already exist
    if Category.query.first():
        return
    
    logging.info("Initializing sample data...")
    
    # Create categories
    categories = [
        ('PT', 'Pottery'),
        ('JW', 'Jewelry'),
        ('TX', 'Textiles'),
        ('WD', 'Woodwork'),
        ('HM', 'Home Decor'),
        ('SC', 'Sculptures')
    ]
    
    for code, name in categories:
        category = Category(code=code, name=name)
        db.session.add(category)
    
    db.session.commit()
    
    # Create sample items
    pottery_cat = Category.query.filter_by(code='PT').first()
    jewelry_cat = Category.query.filter_by(code='JW').first()
    textiles_cat = Category.query.filter_by(code='TX').first()
    woodwork_cat = Category.query.filter_by(code='WD').first()
    home_decor_cat = Category.query.filter_by(code='HM').first()
    sculptures_cat = Category.query.filter_by(code='SC').first()
    
    sample_items = [
        # Pottery
        {
            'title': 'Handcrafted Ceramic Vase',
            'slug': 'handcrafted-ceramic-vase',
            'description': 'Beautiful ceramic vase handcrafted by skilled artisans using traditional techniques. Perfect for displaying fresh flowers or as a decorative piece.',
            'price': 45.00,
            'discount_price': 35.00,
            'category_id': pottery_cat.id,
            'label': 'P'
        },
        {
            'title': 'Rustic Clay Bowls Set',
            'slug': 'rustic-clay-bowls-set',
            'description': 'Set of 4 rustic clay bowls, perfect for serving or as decorative pieces. Each bowl is unique with natural variations.',
            'price': 60.00,
            'category_id': pottery_cat.id,
            'label': 'S'
        },
        
        # Jewelry
        {
            'title': 'Silver Wire Wrapped Pendant',
            'slug': 'silver-wire-wrapped-pendant',
            'description': 'Elegant silver wire wrapped pendant with natural stone. Handcrafted with attention to detail and comes with a chain.',
            'price': 35.00,
            'discount_price': 28.00,
            'category_id': jewelry_cat.id,
            'label': 'D'
        },
        {
            'title': 'Bohemian Beaded Earrings',
            'slug': 'bohemian-beaded-earrings',
            'description': 'Colorful bohemian-style beaded earrings made with natural materials. Perfect for adding a pop of color to any outfit.',
            'price': 25.00,
            'category_id': jewelry_cat.id,
            'label': 'P'
        },
        
        # Textiles
        {
            'title': 'Hand-woven Wool Scarf',
            'slug': 'hand-woven-wool-scarf',
            'description': 'Soft and warm hand-woven wool scarf in traditional patterns. Made from 100% natural wool using traditional weaving techniques.',
            'price': 85.00,
            'discount_price': 70.00,
            'category_id': textiles_cat.id,
            'label': 'P'
        },
        {
            'title': 'Embroidered Cotton Table Runner',
            'slug': 'embroidered-cotton-table-runner',
            'description': 'Beautiful embroidered cotton table runner featuring traditional motifs. Perfect for dining room decoration.',
            'price': 40.00,
            'category_id': textiles_cat.id,
            'label': 'S'
        },
        
        # Woodwork
        {
            'title': 'Carved Wooden Bowl',
            'slug': 'carved-wooden-bowl',
            'description': 'Hand-carved wooden bowl made from sustainable hardwood. Each bowl is unique with beautiful natural grain patterns.',
            'price': 55.00,
            'category_id': woodwork_cat.id,
            'label': 'P'
        },
        {
            'title': 'Wooden Cutting Board Set',
            'slug': 'wooden-cutting-board-set',
            'description': 'Set of 3 wooden cutting boards in different sizes. Made from bamboo, perfect for kitchen use and eco-friendly.',
            'price': 75.00,
            'discount_price': 65.00,
            'category_id': woodwork_cat.id,
            'label': 'D'
        },
        
        # Home Decor
        {
            'title': 'Macrame Wall Hanging',
            'slug': 'macrame-wall-hanging',
            'description': 'Beautiful macrame wall hanging made with natural cotton rope. Adds a bohemian touch to any room.',
            'price': 50.00,
            'category_id': home_decor_cat.id,
            'label': 'P'
        },
        {
            'title': 'Ceramic Candle Holders Set',
            'slug': 'ceramic-candle-holders-set',
            'description': 'Set of 3 ceramic candle holders in different heights. Creates a beautiful ambiance and perfect for home decoration.',
            'price': 38.00,
            'discount_price': 30.00,
            'category_id': home_decor_cat.id,
            'label': 'S'
        },
        
        # Sculptures
        {
            'title': 'Abstract Stone Sculpture',
            'slug': 'abstract-stone-sculpture',
            'description': 'Hand-carved abstract stone sculpture. A unique piece of art that adds sophistication to any space.',
            'price': 120.00,
            'category_id': sculptures_cat.id,
            'label': 'D'
        },
        {
            'title': 'Miniature Bronze Figurine',
            'slug': 'miniature-bronze-figurine',
            'description': 'Detailed miniature bronze figurine crafted using traditional casting techniques. Perfect for collectors.',
            'price': 95.00,
            'discount_price': 80.00,
            'category_id': sculptures_cat.id,
            'label': 'P'
        }
    ]
    
    for item_data in sample_items:
        item = Item(**item_data)
        db.session.add(item)
    
    # Create sample user
    user = User(
        username='demo_user',
        email='user@example.com',
        first_name='Demo',
        last_name='User'
    )
    user.set_password('password123')
    db.session.add(user)
    
    # Create sample coupons
    coupons = [
        ('WELCOME10', 10.00),
        ('SAVE20', 20.00),
        ('ARTISAN15', 15.00)
    ]
    
    for code, amount in coupons:
        coupon = Coupon(code=code, amount=amount)
        db.session.add(coupon)
    
    db.session.commit()
    logging.info("Sample data initialized successfully!")
