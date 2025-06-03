from flask import render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy import or_, and_
from datetime import datetime
from core import bp
from models import Item, Category, Order, OrderItem, User, Coupon
from forms import CheckoutForm, CouponForm
from app import db
import logging


def get_or_create_order():
    """Get or create an order for the current session or user"""
    if 'user_id' in session:
        # User is logged in
        order = Order.query.filter_by(user_id=session['user_id'], ordered=False).first()
        if not order:
            order = Order(user_id=session['user_id'])
            db.session.add(order)
            db.session.commit()
    else:
        # Anonymous user - use session
        if 'session_id' not in session:
            import uuid
            session['session_id'] = str(uuid.uuid4())
        
        order = Order.query.filter_by(session_id=session['session_id'], ordered=False).first()
        if not order:
            order = Order(session_id=session['session_id'])
            db.session.add(order)
            db.session.commit()
    
    return order




@bp.route('/')
def home():
    # Get featured items (items with discount_price)
    featured_items = Item.query.filter(Item.discount_price.isnot(None)).limit(4).all()
    
    # Get latest items
    latest_items = Item.query.order_by(Item.date_added.desc()).limit(8).all()
    
    # Get categories for display
    categories = Category.query.all()
    
    return render_template('home.html', 
                         featured_items=featured_items,
                         latest_items=latest_items,
                         categories=categories)


@bp.route('/products')
def products():
    # Get all categories for sidebar
    categories = [(cat.code, cat.name) for cat in Category.query.all()]
    
    # Start with base query
    query = Item.query
    
    # Filter by category if specified
    category_filter = request.args.get('category')
    if category_filter:
        query = query.join(Category).filter(Category.code == category_filter)
    
    # Filter by price range
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    if min_price is not None:
        query = query.filter(
            or_(
                and_(Item.discount_price.isnot(None), Item.discount_price >= min_price),
                and_(Item.discount_price.is_(None), Item.price >= min_price)
            )
        )
    
    if max_price is not None:
        query = query.filter(
            or_(
                and_(Item.discount_price.isnot(None), Item.discount_price <= max_price),
                and_(Item.discount_price.is_(None), Item.price <= max_price)
            )
        )
    
    # Sort products
    sort_by = request.args.get('sort', 'default')
    if sort_by == 'price_asc':
        query = query.order_by(Item.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Item.price.desc())
    elif sort_by == 'name_asc':
        query = query.order_by(Item.title.asc())
    elif sort_by == 'name_desc':
        query = query.order_by(Item.title.desc())
    else:
        query = query.order_by(Item.date_added.desc())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    items = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('products.html', 
                         items=items,
                         categories=categories)


@bp.route('/product/<slug>')
def product_detail(slug):
    item = Item.query.filter_by(slug=slug).first_or_404()
    return render_template('product_detail.html', item=item)


@bp.route('/add-to-cart/<slug>')
def add_to_cart(slug):
    item = Item.query.filter_by(slug=slug).first_or_404()
    order = get_or_create_order()
    
    # Check if item already in cart
    order_item = OrderItem.query.filter_by(order_id=order.id, item_id=item.id).first()
    
    if order_item:
        # Increase quantity
        order_item.quantity += 1
    else:
        # Add new item
        order_item = OrderItem(order_id=order.id, item_id=item.id, quantity=1)
        db.session.add(order_item)
    
    db.session.commit()
    flash(f'{item.title} added to cart!', 'success')
    
    # Redirect back to the referring page or products
    return redirect(request.referrer or url_for('core.products'))


@bp.route('/remove-from-cart/<slug>')
def remove_from_cart(slug):
    item = Item.query.filter_by(slug=slug).first_or_404()
    order = get_or_create_order()
    
    order_item = OrderItem.query.filter_by(order_id=order.id, item_id=item.id).first()
    if order_item:
        db.session.delete(order_item)
        db.session.commit()
        flash(f'{item.title} removed from cart!', 'info')
    
    return redirect(url_for('core.cart'))


@bp.route('/remove-single-item-from-cart/<slug>')
def remove_single_item_from_cart(slug):
    item = Item.query.filter_by(slug=slug).first_or_404()
    order = get_or_create_order()
    
    order_item = OrderItem.query.filter_by(order_id=order.id, item_id=item.id).first()
    if order_item:
        if order_item.quantity > 1:
            order_item.quantity -= 1
        else:
            db.session.delete(order_item)
        db.session.commit()
    
    return redirect(url_for('core.cart'))


@bp.route('/cart')
def cart():
    order = get_or_create_order()
    return render_template('cart.html', order=order)


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    order = get_or_create_order()
    
    if not order.items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('core.products'))
    
    form = CheckoutForm()
    
    if form.validate_on_submit():
        # Store shipping information
        shipping_info = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'address': form.address.data,
            'city': form.city.data,
            'state': form.state.data,
            'zip_code': form.zip_code.data,
            'phone': form.phone.data
        }
        
        # Store in session for payment processing
        session['shipping_info'] = shipping_info
        
        # For demo purposes, complete the order
        order.ordered = True
        order.ordered_date = datetime.utcnow()
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        
        # Clear the cart session
        if 'session_id' in session:
            session.pop('session_id', None)
        
        return redirect(url_for('core.home'))
    
    return render_template('checkout.html', form=form, order=order)


@bp.route('/add-coupon', methods=['POST'])
def add_coupon():
    form = CouponForm()
    if form.validate_on_submit():
        code = form.code.data.upper()
        coupon = Coupon.query.filter_by(code=code, active=True).first()
        
        if coupon:
            # Store coupon in session
            session['coupon_code'] = code
            flash(f'Coupon "{code}" applied successfully!', 'success')
        else:
            flash('Invalid coupon code.', 'error')
    
    return redirect(url_for('core.cart'))


# Template context processors
@bp.app_context_processor
def inject_cart_count():
    """Make cart count available in all templates"""
    try:
        order = get_or_create_order()
        cart_count = order.get_item_count() if order else 0
    except:
        cart_count = 0
    
    return dict(cart_count=cart_count)


# Error handlers
@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
