from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from datetime import datetime
from .models import db, User, Post, Task, Reply, WaitingList
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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
        category = request.args.get('category')
        if category:
            posts = Post.query.filter_by(category=category).order_by(Post.created_at.desc()).all()
        else:
            posts = Post.query.order_by(Post.created_at.desc()).all()
        category = ['Daily', 'Petsitting', 'Adoption']
        #posts = Post.query.order_by(Post.created_at.desc()).all()  
        return render_template('index.html', page_name='Home', nav=nav, posts=posts, category=category)

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
                user_image=f'/static/image/avatars/{user_image}' if user_image else None
            )

            db.session.add(new_user)
            db.session.commit()

            # Log the user in
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', page_name='Signup', nav=nav)

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

    @app.route('/reply/<int:post_id>', methods=['POST'])
    @login_required
    def post_reply(post_id):
        content = request.form.get('content')
        parent_reply_id = request.form.get('parent_reply_id')  # Optional, for nested replies
        if content:
            try:
                new_reply = Reply(
                    post_id=post_id,
                    reply_by=current_user.id,
                    parent_reply_id=parent_reply_id if parent_reply_id else None,
                    content=content,
                    post_at=datetime.utcnow()
                )
                db.session.add(new_reply)
                db.session.commit()
                flash('Replied successfully!', 'success')
                saved_reply = Reply.query.filter_by(id=new_reply.id).first()
                if saved_reply:
                    print("Reply saved:", saved_reply.content)

            except Exception as e:
                db.session.rollback()
                flash('Failed to post reply: ' + str(e), 'error')
        else:
            flash('Reply content cannot be empty!', 'error')

        return redirect(url_for('post_detail', post_id=post_id))

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
            'components/nav_logged_out.html')
        if request.method == 'POST':
            current_user.username = request.form.get('username', current_user.username)
            current_user.email = request.form.get('email', current_user.email)
            current_user.phone = request.form.get('phone', current_user.phone)
            current_user.gender = request.form.get('gender', current_user.gender)
            current_user.postcode = request.form.get('postcode', current_user.postcode)
            current_user.pet_type = request.form.get('petType', current_user.pet_type)
            new_image = request.form.get('user_image')
            if new_image:
                current_user.user_image = new_image
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
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
                    post_images_dir = os.path.join("/static/image/uploads", str(new_post.id))
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

                    # Add entry to the WaitingList
                    waiting_list_entry = WaitingList(
                        task_id=new_post.id,
                        user_id=current_user.id,
                        applied_at=datetime.utcnow()
                    )
                    db.session.add(waiting_list_entry)

                db.session.commit()
                flash('Post created successfully!', 'success')
                return redirect(url_for('home'))

            except Exception as e:
                db.session.rollback()  # Rollback the session in case of error
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('post_create'))

        return render_template('post_create.html', page_name='PostCreate', nav=nav)

    @app.route('/delete_post/<int:post_id>', methods=['POST'])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if current_user.id != post.created_by:
            flash('You are not authorized to delete this post.', 'error')
            return redirect(url_for('post_detail', post_id=post_id))
        try:
            db.session.delete(post)  # Deleting the post should cascade and delete all associated replies
            db.session.commit()
            flash('Post and all associated replies deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error deleting post: ' + str(e), 'error')
        return redirect(url_for('home'))

    @app.route('/delete_reply/<int:reply_id>', methods=['POST'])
    @login_required
    def delete_reply(reply_id):
        reply = Reply.query.get_or_404(reply_id)
        if current_user.id != reply.reply_by:
            flash('You are not authorized to delete this reply.', 'error')
            return redirect(url_for('post_detail', post_id=reply.post_id))
        try:
            db.session.delete(reply)  # Deleting the reply should cascade and delete all child replies
            db.session.commit()
            flash('Reply and all child replies deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error deleting reply: ' + str(e), 'error')
        return redirect(url_for('post_detail', post_id=reply.post_id))

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

        if current_user.is_authenticated:
            nav = render_template('components/nav_logged_in.html')
        else:
            nav = render_template('components/nav_logged_out.html')
        return render_template('search_results.html', query=query, posts=posts, nav=nav)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error_pages/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error_pages/500.html'), 500

    @app.route('/cause_500')
    def cause_500():
        raise Exception("Intentional Error")

    @app.route('/post/<int:post_id>')
    def post_detail(post_id):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        post = Post.query.get_or_404(post_id)
        nav = render_template('components/nav_logged_in.html') if current_user.is_authenticated else render_template(
        'components/nav_logged_out.html')
        return render_template('post_detail.html', post=post, nav=nav)
    
    @app.route('/like_post/<int:post_id>', methods=['POST'])
    @login_required
    def like_post(post_id):
        post = Post.query.get_or_404(post_id)
        post.like_count += 1
        db.session.commit()
        return jsonify({'like_count': post.like_count})
