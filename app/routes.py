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
    def reply():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
        return render_template('reply.html', page_name='Reply',nav=nav)
      
    @app.route('/users')
    def users():
        users = User.query.all()
        return render_template('users.html', page_name='Users', users=users)
    
    @app.route('/profile')
    def profile():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
        return render_template('profile.html',page_name='Profile',nav=nav)
    
    @app.route('/postcreate')
    def postcreate():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template('components/nav_logged_out.html')
        return render_template('post_create.html',page_name='PostCreate', nav=nav)

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