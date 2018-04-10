

# Home Route 
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Movie, Rating, connect_to_db, db


app = Flask(__name__)

app.secret_key = 'ABC123'

app.jinja_env.undefined = StrictUndefined


# =============================================================================
# User Login / Register New User


@app.route('/login') or @app.route('/') ? 
def user_login():
    """Login new user"""

#     users = User.query.all()
    return render_template('login.html', users=users)

@app.route('/register')
def register_user():
    """ Register New User """

    return render_template('register_user.html', users=users)

# =============================================================================
# Homepage and Search View

@app.route('/')
def default_view():
    """ Default top trending coverage """

    return render_template('homepage.html')

@app.route('/<search-term>')
def search_term():
    """ Update visual to show new coverage for search term """

    return redirect ("/")

# =============================================================================
# About

@app.route('/aboutnewsflash')
def about_us():
    """list a brief description about Newsflash"""

     return render_template('about.html', users=users)

# =============================================================================
# Favorites

# @app.route('/favorites')
# def favorite_searches():
#     """ Show list of favorite searches for user"""