from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
@main.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # check if the user is present in db
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for('main.dashboard'))  # Successful login
        else:
            return render_template('login.html', error="Invalid credentials")
        

    return render_template('login.html')

# Route for signup page
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user or (password!=confirm_password):
            return render_template('signup.html', error="Username already exists")

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Add the new user to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful signup
        return redirect(url_for('main.login'))

    return render_template('signup.html')

# Dashboard route (after successful login)
@main.route('/dashboard')
def dashboard():
    return '<h1>Welcome to your dashboard!</h1>'

