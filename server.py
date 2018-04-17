
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Search, Outlet, connect_to_db, db
import os
import requests

API_KEY = os.environ['API_KEY']

app = Flask(__name__)

app.secret_key = 'ABC'

app.jinja_env.undefined = StrictUndefined

# =============================================================================
# Homepage and Search View

@app.route('/', methods=['GET'])
def default_view():
    """ Default top trending coverage - possibly also combine with search term? """

    return render_template('homepage.html')

@app.route('/newsbykeyword')
def search_term():
    # methods=['POST']
    """ Update visual to show new coverage for search term """

#     search = request.form.get('fav_keyword')

#     if email in session:
#         if User.query.filter(User.email == session['email']).first() && Search.query.filter(Search.search_term == fav_keyword).all() is None:
#         search_term = Search(search_term=fav_keyword)
#         db.session.add(search_term)
#         db.session.commit()
#         return redirect('/')

    return render_template("search_view.html")

# =============================================================================
# User Login / User Logout / Register New User

@app.route('/login', methods=['GET']) 
def login_form():
    """Displays Login Form"""

    # if 'email' in session:
    #     del session['email']

    return render_template('login.html')

@app.route('/login', methods=['POST']) 
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

    users = User.query.all()
    return render_template('login.html')

@app.route('/logout')
def user_logout():
    """Logout user"""

    if 'email' in session:
        del session['email']
        flash ('Logged out')

    return redirect('/')

@app.route('/register', methods=['GET'])
def register_form():
    """Display register form"""

    return render_template('register_user.html')

@app.route('/register', methods=['POST'])
def register_user():
    """ Register New User """

    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter(User.email == email).first() is None:
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['email'] = email
        flash('Registered as {}'.format(email))
        return redirect('/')

    flash('User already exists')
    return redirect('/login')

# =============================================================================
# Json Route

# @app.route('/trending_info.json')
# def return_trending_json_from_api():

#     """Pull top trending articles from News API"""
#     url = ('https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal,the-new-york-times,bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,usa-today,politico,cnbc,engadget,nbc-news,cbs-news,abc-news,associated-press,fortune&apiKey={}'.format(API_KEY))
#     response = requests.get(url)

#     return jsonify(response.json())

# @app.route('/search_info.json')
# def return_search_json_from_api():

#     """Pull top trending articles from News API"""
#     url = ('https://newsapi.org/v2/top-headlines?language=en&q={}&sortBy=relevancy&apiKey={}'.format({{ keyword }}, API_KEY))
#     response = requests.get(url)

#     return jsonify(response.json())


# =============================================================================
# User 

@app.route('/users')
def view_all_users():
    """Display users for test"""

    users = User.query.all()

    return render_template('user.html', users=users)

# =============================================================================
# About

@app.route('/aboutnewsflash')
def about_us():
    """list a brief description about Newsflash"""

    return render_template('about.html')

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')