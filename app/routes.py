from flask import render_template, request, redirect, url_for
from datetime import datetime
from models import db, User
from flask_login import LoginManager, login_user, logout_user
from app import app


def init_app_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html', title='Paw Forum', page_name='Home')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']  # This now gets hashed automatically
            phone = request.form.get('phone', None)
            gender = request.form.get('gender', None)
            postcode = request.form.get('postcode', None)
            user_image = request.form.get('user_image', 'avatar1.png')

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

            return redirect(url_for('home'))
        else:
            return render_template('Signup.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                return 'Invalid username or password'
        return render_template('SignIn.html')
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))
