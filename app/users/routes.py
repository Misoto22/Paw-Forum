from flask import Blueprint, render_template, redirect, request, url_for
from .forms import RegistrationForm, LoginForm
from database.models import User, db

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Form processing logic
        # Redirect to home after registration
        return redirect(url_for('users.login'))
    return render_template('register.html')

@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authentication logic
        # Redirect to home after login
        return redirect(url_for('main.home'))
    return render_template('login.html')
