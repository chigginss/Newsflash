
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Search, Outlet, connect_to_db, db
import os
import requests

#logout not working
# API_KEY = os.environ['API_KEY']

app = Flask(__name__)

app.secret_key = 'ABC'

app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# =============================================================================
# Homepage 

@app.route('/', methods=['GET'])
def default_view():
    """ Default top trending coverage"""


    return render_template('homepage.html')

# =============================================================================
# Search Views - form and visual 

@app.route('/searchbykeyword', methods=['GET'])
def search_term():
    """ Update visual to show new coverage for search term """

    return render_template('search_for_term.html')

@app.route('/topsearch.json', methods=['POST'])
def search_for_term():
    """ Update visual to show new coverage for search term """
        
    keyword = request.form.get('keyword')

    #     #search for search_terms in Search table if user_id (that matches email in User table) also matches user_id in User_Search table.
    #     #If none exist, add search_term to Search table that corresponds to User_id in User_Search table


#how will they view favorites? entire list or just top 3 - how will they decide 
#case sensitive - for searches 

    # check to see if search matches that user's searches (search_terms associated with specific user_id)
    # if not, add for that specific user_id
    # if session['user_id'] 
    # User_Search.query.filter(User_Search.user_id, User_Search.search_id).all() 
    # if User_Search.search_id matches Search.search_id 
    #Search.query.filter(Search.search_term == keyword).first() is None:
    #         search_term = Search(search_term=keyword)
    #         search_id = User_Search(search_id=search_id)
    #         db.session.add(search_term)
    #         db.session.add(search_id)
    #         db.session.commit()
    #         flash('New search added')
    
        #pageSize=50&
    r = requests.get(('https://newsapi.org/v2/top-headlines?language=en&q={}&sortBy=relevancy'+
                     '&apiKey=1ec5e2d27afa46efaf95cfb4c8938f37').format(keyword))

    top_search_json = r.json()
    # print top_search_json
    # print top_trending_json
    top_searches = top_search_json['articles']
    # print top_articles
    for i in range(len(top_searches)):
        source_name = top_searches[i].get('source')['name']

        # pull objects from newsflashdb
        data = Outlet.query.filter(Outlet.outlet_name == source_name).first()

        # add popularity and bias into json
        if data is not None:
            top_searches[i]['popularity'] = data.outlet_popularity
            top_searches[i]['bias'] = data.outlet_bias
        else:
            top_searches[i]['popularity'] = False
            top_searches[i]['bias'] = False

    return jsonify(top_searches)

    # searches = Search.query.all()

# @app.route('/newsbykeyword', methods=['GET'])
# def search_news_coverage():
#     """ Display search term form """

#     return render_template('search_view.html')

# =============================================================================
# JSON routes for top and search coverage

@app.route('/toptrending.json')
def json_data():
    """Combine News API and database data"""

    r = requests.get("https://newsapi.org/v2/top-headlines?sources=the-wall-street-journal,the-new-york-times,"+
                      "bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,"+
                      "usa-today,politico,cnbc,engadget,nbc-news,cbs-news,abc-news,associated-press,fortune&apiKey=1ec5e2d27afa46efaf95cfb4c8938f37")
    top_trending_json = r.json()

    # print top_trending_json
    top_articles = top_trending_json['articles']
    # print top_articles
    for i in range(len(top_articles)):
        source_name = top_articles[i].get('source')['name']
        # print source_name  
        # pull objects from newsflashdb
        data = Outlet.query.filter(Outlet.outlet_name == source_name).first()
        # print data
        # add popularity and bias into json
        if data is not None:
            top_articles[i]['popularity'] = data.outlet_popularity
            top_articles[i]['bias'] = data.outlet_bias
        else:
            top_articles[i]['popularity'] = False
            top_articles[i]['bias'] = False

    return jsonify(top_articles)

# =============================================================================
# User Login / User Logout / Register New User

@app.route('/login', methods=['GET']) 
def login_form():
    """Displays Login Form"""


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
        session['user_id'] = user.user_id
        flash('Logged in as {}'.format(user.email))
        return redirect('/')

    flash('Invalid password')
    return redirect('/login')

    users = User.query.all()
    return render_template('login.html')

@app.route('/logout')
def user_logout():
    """Logout user"""

    if 'user_id' in session:
        del session['user_id']
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
        session['user_id'] = user.user_id
        flash('Registered as {}'.format(email))
        return redirect('/')

    flash('User already exists')
    return redirect('/login')


# =============================================================================
# User 

# @app.route('/users')
# def view_all_users():
#     """Display users for test"""

#     users = User.query.all()

#     return render_template('user.html', users=users)

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