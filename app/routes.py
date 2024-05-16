from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from .models import db, User, Post
from flask_login import login_user, logout_user, login_required, current_user

def init_app_routes(app):
    @app.route('/')
    def home():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
        return render_template('index.html', title='Paw Forum', page_name='Home', nav=nav)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            phone = request.form.get('phone', None)
            gender = request.form.get('gender', None)
            postcode = request.form.get('postcode', None)
            user_image = request.form.get('user_image', 'avatar1.png')

            # Validate required fields
            if not username or not email or not password:
                flash('All fields are required', 'error')
                return redirect(url_for('signup'))
                
            # Validate email format
            if '@' not in email or '.' not in email:
                flash('Invalid email format', 'error')
                return redirect(url_for('signup'))

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
            return render_template('signup.html', title='Paw Forum', page_name='Signup',nav=nav)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
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
        return render_template('login.html', nav=nav)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/reply')
    @login_required
    def reply():
        nav = render_template('components/nav_logged_in.html')
        return render_template('reply.html', page_name='Reply', nav=nav)
      
    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', page_name='Users', users=users)
    
    @app.route('/profile')
    @login_required
    def profile():
        nav = render_template('components/nav_logged_in.html')
        return render_template('profile.html', page_name='Profile', nav=nav)
    
    @app.route('/postcreate')
    @login_required
    def postcreate():
        nav = render_template('components/nav_logged_in.html')
        return render_template('post_create.html', page_name='PostCreate', nav=nav)

    @app.route('/search')
    def search():
        query = request.args.get('query')
        if query:
            posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
        else:
            posts = []
        return render_template('search_results.html', query=query, posts=posts)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_pages/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error_pages/500.html'), 500

    @app.route('/cause_500')
    def cause_500():
        raise Exception("Intentional Error")
