from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from .models import db, User
from flask_login import login_user, logout_user, login_required


def init_app_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html', title='Paw Forum', page_name='Home')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            phone = request.form.get('phone', None)
            gender = request.form.get('gender', None)
            postcode = request.form.get('postcode', None)
            user_image = request.form.get('user_image', 'avatar1.png')

            # Check if the username or email already exists
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                flash('Username or Email already exists', 'error')
                return redirect(url_for('signup'))

            # Create new User object with hashed password
            new_user = User(
                username=username,
                email=email,
                password=password,  # This is automatically hashed by the setter method
                phone=phone,
                gender=gender,
                postcode=postcode,
                join_at=datetime.utcnow(),
                user_image=f'/static/image/avatar/{user_image}' if user_image else None
            )

            db.session.add(new_user)
            db.session.commit()

            # Log the user in
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', title='Paw Forum', page_name='Signup')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'error')
                return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/reply')
    def reply():
        return render_template('reply.html', title='Paw Forum', page_name='Reply')

    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', users=users)
