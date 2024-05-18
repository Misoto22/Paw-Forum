from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from datetime import datetime
from .models import db, User, Post, Task, Reply, WaitingList, PostLike, ReplyLike, Activity
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename
from .config import Config
from werkzeug.security import generate_password_hash

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


    # Define the signup route
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

            # log the activity
            new_activity = Activity(
                user_id=new_user.id,
                action='has signed up!',
                target_user_id=None
            )

            db.session.add(new_activity)
            db.session.commit()

            # Log the user in
            login_user(new_user)
            flash('Registration successful!', 'success')
            return redirect(url_for('home'))
        else:
            return render_template('signup.html', page_name='Signup', nav=nav)


    # Define the login route， and check if the user is authenticated
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


    # Define the logout route
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))
    
    
    # Define the profile route
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

            # log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action='has updated profile!',
                target_user_id=None
            )

            db.session.add(new_activity)
            db.session.commit()

            return redirect(url_for('profile'))
        return render_template('profile.html', page_name='Profile', nav=nav)


    # Define the post_create route
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
                image_file = request.files.get('image')  # Only allow one image

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

                # Check if an image was uploaded
                if image_file and allowed_file(image_file.filename):

                    # Rename the image to avoid duplicates
                    original_filename = secure_filename(image_file.filename)
                    file_ext = original_filename.rsplit('.', 1)[1].lower()
                    new_filename = f"{generate_password_hash(original_filename + str(datetime.utcnow()))[:20]}.{file_ext}"
                    image_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)
                    image_file.save(image_path)

                    new_post.image_name = new_filename  # Save the new image name to the post

                if is_task:
                    new_task = Task(
                        id=new_post.id,  # Same ID as the post
                        status=True,  # 'open'
                        assigned_to=None
                    )
                    db.session.add(new_task)

                db.session.commit()
                flash('Post created successfully!', 'success')

                # Log the activity
                new_activity = Activity(
                    user_id=current_user.id,
                    action='created post ' + str(new_post.id)
                )
                db.session.add(new_activity)

                if is_task:
                    new_activity = Activity(
                        user_id=current_user.id,
                        action='created task ' + str(new_post.id)
                    )
                    db.session.add(new_activity)

                db.session.commit()

                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating post: {e}', 'danger')
                return redirect(url_for('post_create'))

        return render_template('post_create.html', nav=nav)

    # Define the post detail route
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

                # Log the activity
                new_activity = Activity(
                    user_id=current_user.id,
                    action='replied to post ' + str(post_id),
                    target_user_id=Post.query.get(post_id).created_by
                )
                db.session.add(new_activity)
                db.session.commit()
                
            except Exception as e:
                db.session.rollback()
                flash('Failed to post reply: ' + str(e), 'error')
        else:
            flash('Reply content cannot be empty!', 'error')

        return redirect(url_for('post_detail', post_id=post_id))
            
    # Define the delete post route
    @app.route('/delete_post/<int:post_id>', methods=['POST'])
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        
        if current_user.id != post.created_by:
            return jsonify({'error': 'You are not authorized to delete this post.'}), 403

        try:
            # Delete associated image from the filesystem
            if post.image_name:
                image_path = os.path.join(Config.UPLOAD_FOLDER, post.image_name)
                if os.path.exists(image_path):
                    os.remove(image_path)

            # Deleting the post should cascade and delete all associated replies
            db.session.delete(post)
            db.session.commit()

            # Log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action='deleted post ' + str(post_id)
            )
            db.session.add(new_activity)
            db.session.commit()

            return jsonify({'success': 'Post and all associated replies deleted successfully!'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error deleting post: ' + str(e)}), 500    

    # Define the delete reply route
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

            # Log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action='deleted reply ' + str(reply_id),
            )
            db.session.add(new_activity)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash('Error deleting reply: ' + str(e), 'error')
        return redirect(url_for('post_detail', post_id=reply.post_id))
    
    # Define the like post route
    @app.route('/like_post/<int:post_id>', methods=['POST'])
    @login_required
    def like_post(post_id):
        post = Post.query.get_or_404(post_id)
        like = PostLike.query.filter_by(user_id=current_user.id, post_id=post_id).first()

        try:
            if like:
                db.session.delete(like)
                post.like_count -= 1
                action = 'unliked'
            else:
                new_like = PostLike(user_id=current_user.id, post_id=post_id)
                db.session.add(new_like)
                post.like_count += 1
                action = 'liked'
            
            db.session.commit()

            # Log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action=f'{action} post {post_id}',
                target_user_id=post.user.id
            )
            db.session.add(new_activity)
            db.session.commit()

            return jsonify({'like_count': post.like_count, 'liked': not bool(like)})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/like_reply/<int:reply_id>', methods=['POST'])
    @login_required
    def like_reply(reply_id):
        reply = Reply.query.get_or_404(reply_id)
        like = ReplyLike.query.filter_by(user_id=current_user.id, reply_id=reply_id).first()

        try:
            if like:
                db.session.delete(like)
                reply.like_count -= 1
                action = 'unliked'
            else:
                new_like = ReplyLike(user_id=current_user.id, reply_id=reply_id)
                db.session.add(new_like)
                reply.like_count += 1
                action = 'liked'
            
            db.session.commit()

            # Log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action=f'{action} reply {reply_id}',
                target_user_id=reply.user.id
            )
            db.session.add(new_activity)
            db.session.commit()

            return jsonify({'like_count': reply.like_count, 'liked': not bool(like)})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500



    # Define the apply task route
    @app.route('/apply_task/<int:task_id>', methods=['POST'])
    @login_required
    def apply_task(task_id):
        try:
            new_application = WaitingList(
                task_id=task_id,
                user_id=current_user.id,
                applied_at=datetime.utcnow()
            )
            db.session.add(new_application)
            db.session.commit()
            flash('Applied to task successfully!', 'success')

            # Log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action=f'applied to task {task_id}'
            )
            db.session.add(new_activity)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash('Failed to apply to task: ' + str(e), 'error')

        return redirect(url_for('task_detail', task_id=task_id))


    # Define the close task route
    @app.route('/close_task/<int:task_id>', methods=['POST'])
    @login_required
    def close_task(task_id):
        task = Task.query.get_or_404(task_id)
        post = Post.query.get_or_404(task.id)
        if current_user.id != post.created_by:
            flash('You are not authorized to close this task.', 'error')
            return redirect(url_for('task_detail', task_id=task_id))

        try:
            task.status = False
            db.session.commit()
            flash('Task closed successfully!', 'success')

            # Log the activity
            new_activity = Activity(
                user_id=current_user.id,
                action=f'closed task {task_id}'
            )
            db.session.add(new_activity)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash('Failed to close task: ' + str(e), 'error')

        return redirect(url_for('task_detail', task_id=task_id))


    # Define the search route
    @app.route('/search')
    def search():
        query = request.args.get('query')
        if query:
            query = query[:100]  # Limit the query to a maximum of 100 characters
            posts = Post.query.join(User).filter(
            Post.title.ilike(f'%{query}%') |
            Post.content.ilike(f'%{query}%') |
            User.username.ilike(f'%{query}%')
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
    

