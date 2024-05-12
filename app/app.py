from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask import url_for, redirect, render_template
from werkzeug.utils import secure_filename
from model import db, User, Post, Reply, Task, Activity
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


# Create the Flask app
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
# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # The route name for your login view

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



# Create a Registration Form
@app.route('/register', methods=['GET', 'POST'])
def register():
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
        return render_template('register.html')



# Main
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
