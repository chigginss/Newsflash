

# Home Route 
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Search, Outlet, connect_to_db, db

app = Flask(__name__)

app.secret_key = 'ABC123'

app.jinja_env.undefined = StrictUndefined

# =============================================================================
# User Login / User Logout / Register New User

@app.route('/login') 
# or @app.route('/') ? 
def user_login():
    """Login user"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User not found')
        return redirect('/login')

    if password == user.password:
        session['email'] = email
        flash('Logged in as {}'.format(email))
        return redirect('/')

    flash('Invalid password')
    return redirect('/login')

#     users = User.query.all()
    return render_template('login.html')

@app.route('/logout')
def user_logout():
    """Logout user"""

    if 'email' in session:
        del session['email']
        flash ('Logged out')

    return redirect('/login')

@app.route('/register')
def register_user():
    """ Register New User """

    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter(User.email == email).first() is None:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['email'] = email
        flash('Logged in')
        return redirect('/')

    flash('User already exists')
    return redirect('/login')

    return render_template('register_user.html')

# =============================================================================
# Homepage and Search View

@app.route('/')
def default_view():
    """ Default top trending coverage - possible also search term? """

    return render_template('homepage.html')

# @app.route('/<search-term>')
# def search_term():
#     """ Update visual to show new coverage for search term """

#     search = request.form.get('search')

#     # render visual for that term?
#     return redirect ("/")

# =============================================================================
# About

@app.route('/aboutnewsflash')
def about_us():
    """list a brief description about Newsflash"""

    return render_template('about.html')
