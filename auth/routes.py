from flask import render_template, request, redirect, url_for, flash, session
from auth import bp
from models import User
from forms import LoginForm, RegistrationForm
from app import db
from sqlalchemy import text 


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        #user = User.query.filter_by(email=form.email.data).first()
        #if user and user.check_password(form.password.data):
        
        # bagian ini secara sengaja dilemahkan untuk menjadi contoh backend yang lemah terhadap serangan SQL Injection
        email_input = form.email.data
        query = text(f"SELECT * FROM user WHERE email= '{email_input}'")
        result = db.session.execute(query)
        user = result.fetchone()
        
        # tidak ada pengecekan terhadap password disini
        if user :
            # Login successful
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.first_name}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('core.home'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def logout():
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('core.home'))
