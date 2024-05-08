from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask import url_for, redirect, render_template

from werkzeug.utils import secure_filename

# Step 1: Setting Up the Flask Application
app = Flask(__name__)

# Set up the database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up the file upload configuration
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'post')  # Directory where files will be stored
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Initialize the database
db = SQLAlchemy(app)


# Step 2: Defining Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    postcode = db.Column(db.String(10))
    join_at = db.Column(db.DateTime, default=datetime.utcnow)
    pet_type = db.Column(db.String(80))
    user_image = db.Column(db.String(255))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    is_task = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)
    like_count = db.Column(db.Integer, default=0)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reply_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=True)
    content = db.Column(db.Text)
    post_at = db.Column(db.DateTime, default=datetime.utcnow)
    like_count = db.Column(db.Integer, default=0)

class Task(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity = db.Column(db.String(50))
    ip_address = db.Column(db.String(100))
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

class WaitingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

# Step 3: Creating the Database
if __name__ == '__main__':
    db.create_all()  # Creates the database and tables
    app.run(debug=True)




@app.route('/')
def home():
    return 'Hello, World!'


# Step 4: Create a Registration Form
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract data from form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone', None)
        gender = request.form.get('gender', None)
        postcode = request.form.get('postcode', None)
        user_image = request.form.get('user_image', '1.png')  # This would be the filename of the selected image

        # Create new User object
        new_user = User(
            username=username,
            email=email,
            password=password,
            phone=phone,
            gender=gender,
            postcode=postcode,
            join_at=datetime.utcnow(),
            user_image=f'/static/image/user/{user_image}' if user_image else None
        )

        # Add to database session and commit
        db.session.add(new_user)
        db.session.commit()

        # Redirect to a new page, e.g., a profile page or the homepage
        return redirect(url_for('home'))
    else:
        # Render the registration form
        return render_template('register.html')


# Step 4: Handling File Uploads

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


