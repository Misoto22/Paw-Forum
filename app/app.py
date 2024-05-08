from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask import url_for, redirect, render_template
from werkzeug.utils import secure_filename
from model import db, User, Post, Reply, Task, Activity


def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def home():
        return 'Welcome to the Homepage!'
    return app

app = create_app()

# Create a Registration Form
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
        user_image = request.form.get('user_image', 'avatar1.png')  # This would be the filename of the selected image

        # Create new User object
        new_user = User(
            username=username,
            email=email,
            password=password,
            phone=phone,
            gender=gender,
            postcode=postcode,
            join_at=datetime.utcnow(),
            user_image=f'/static/image/avatar/{user_image}' if user_image else None
        )

        # Add to database session and commit
        db.session.add(new_user)
        db.session.commit()

        # Redirect to a new page, e.g., a profile page or the homepage
        return redirect(url_for('home'))
    else:
        # Render the registration form
        return render_template('register.html')
    


# Handling File Uploads

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}








# Main
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
