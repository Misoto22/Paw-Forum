from flask import render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from .models import db, User, Post, Task
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def init_app_routes(app):
    @app.route('/')
    def home():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')
        return render_template('index.html', title='Paw Forum', page_name='Home', nav=nav)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')

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
            return render_template('signup.html', title='Paw Forum', page_name='Signup', nav=nav)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
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
            try:
                title = request.form['title']
                content = request.form['content']
                category = request.form.get('category')
                is_task = 'is_task' in request.form
                images = request.files.getlist('images')

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

                # Check if any images were uploaded
                if images and any(image_file.filename for image_file in images):
                    post_images_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(new_post.id))
                    os.makedirs(post_images_dir, exist_ok=True)

                    for image_file in images:
                        if image_file and allowed_file(image_file.filename):
                            filename = secure_filename(image_file.filename)
                            image_path = os.path.join(post_images_dir, filename)
                            image_file.save(image_path)

                    new_post.image_path = post_images_dir

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

            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('post_create'))

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
