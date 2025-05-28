from app import db
from datetime import datetime
#from argon2 import PasswordHasher
from flask_login import UserMixin

#ph = PasswordHasher()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        #self.password_hash = ph.hash(password,)
        self.password_hash = password


    def check_password(self, password):
        
        return self.password_hash
        """try :
            return ph.verify(self.password_hash, password)
        except :
            return False"""
        
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Relationships
    items = db.relationship('Item', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_price = db.Column(db.Numeric(10, 2), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    label = db.Column(db.String(1), default='P')  # P=Primary, S=Secondary, D=Danger
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='item', lazy=True)
    
    def get_absolute_url(self):
        return f'/product/{self.slug}'
    
    def get_add_to_cart_url(self):
        return f'/add-to-cart/{self.slug}'
    
    def get_remove_from_cart_url(self):
        return f'/remove-from-cart/{self.slug}'
    
    def get_final_price(self):
        if self.discount_price:
            return float(self.discount_price)
        return float(self.price)
    
    def get_label_display(self):
        if self.label == 'P':
            return 'primary'
        elif self.label == 'S':
            return 'secondary'
        elif self.label == 'D':
            return 'danger'
        return 'primary'
    
    def __repr__(self):
        return f'<Item {self.title}>'


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    
    def get_total_item_price(self):
        return self.quantity * float(self.item.price)
    
    def get_total_discount_item_price(self):
        if self.item.discount_price:
            return self.quantity * float(self.item.discount_price)
        return self.get_total_item_price()
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
    
    def __repr__(self):
        return f'<OrderItem {self.item.title} x{self.quantity}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(128), nullable=True)
    ordered = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    ordered_date = db.Column(db.DateTime, nullable=True)
    
    # Shipping Address
    shipping_address = db.Column(db.String(500), nullable=True)
    
    # Payment
    payment_id = db.Column(db.String(100), nullable=True)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def get_total(self):
        total = 0
        for order_item in self.items:
            total += order_item.get_final_price()
        return total
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items)
    
    def __repr__(self):
        return f'<Order {self.id}>'


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Coupon {self.code}>'
