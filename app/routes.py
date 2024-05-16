from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from .models import db, User, Post, Task
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename

def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format")

def validate_postcode(postcode):
    if not postcode.isdigit() or len(postcode) != 4:
        raise ValueError("Invalid postcode")

def init_app_routes(app):
    @app.route('/')
    def home():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')
        return render_template('index.html', title='Paw Forum', page_name='Home', nav=nav)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
        error_message = None
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
                error_message = 'All fields are required'
            else:
                # Validate email format
                try:
                    validate_email(email)
                except ValueError as e:
                    error_message = str(e)

                if not error_message:
                    # Check if the username or email already exists
                    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                        error_message = 'Username or Email already exists'

            if error_message:
                return render_template('signup.html', page_name='Signup', nav=nav, error_message=error_message)

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
            return render_template('signup.html', title='Paw Forum', page_name='Signup', nav=nav)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error_message = None
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                error_message = 'Invalid username or password'
        return render_template('login.html', page_name='Login', nav=nav, error_message=error_message)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/reply')
    def reply():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')
        if not current_user.is_authenticated:
            flash('Please log in to view posts or reply.', 'info')
            return redirect(url_for('login'))
        return render_template('reply.html', page_name='Reply', nav=nav)

    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', page_name='Users', users=users)

    @app.route('/profile')
    def profile():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')
        return render_template('profile.html', page_name='Profile', nav=nav)

    @app.route('/post_create', methods=['GET', 'POST'])
    @login_required
    def post_create():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            category = request.form.get('category')
            is_task = 'is_task' in request.form

            new_post = Post(
                title=title,
                content=content,
                category=category,
                is_task=is_task,
                created_by=current_user.id,
                created_at=datetime.utcnow()
            )

            db.session.add(new_post)
            db.session.flush()  # Flush to assign an ID to new_post

            if is_task:
                new_task = Task(
                    id=new_post.id,  # Same ID as the post
                    status='open',
                    assigned_to=None
                )
                db.session.add(new_task)

            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('home'))

        return render_template('post_create.html', page_name='PostCreate', nav=nav)

    @app.route('/search')
    def search():
        query = request.args.get('query')
        if query:
            posts = Post.query.join(User).filter(
            Post.title.contains(query) | 
            Post.content.contains(query) |
            User.username.contains(query)
        ).all()
            #Only demonstrate part of the matching content
            for post in posts:
                content = post.content
                start_index = content.find(query)
                if start_index != -1:
                    start_index = max(0, start_index - 50)
                    end_index = min(len(content), start_index + len(query) + 50)
                    post.content = '...' + content[start_index:end_index] + '...'
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
