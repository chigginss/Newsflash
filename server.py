
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.security import generate_password_hash, check_password_hash
from model import User, User_Search, Search, Outlet, connect_to_db, db
from datetime import datetime
import pytz
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

# @app.route('/landing', methods=['GET'])
# def landing_view():

        

#     return render_template('landing.html')

@app.route('/', methods=['GET'])
def default_view():
    """ Default top trending coverage"""


    fmt = '%B %d, %Y - %-I:%M %p, %S seconds'
    # pacific = timezone('America/Los_Angeles')
    # datet = datetime.now()
    # dtime = pacific.localize(datet)
    # # fmt = '%B %d, %Y - %H:%M:%S %Z%z'
    # dtime = dtime.strftime(fmt)
    # fmt = '%B %d, %Y - %H:%M:%S %Z%z'
    d = datetime.now()
    timezone = pytz.timezone("America/Los_Angeles")
    d_aware = timezone.localize(d)
    dtime = d_aware.strftime(fmt)

    return render_template('homepage.html',
                            dtime=dtime)


@app.route('/testtest', methods=['GET'])
def default_test_test():
    """ Default top trending coverage"""


    return render_template('test_test_test.html')

# =============================================================================
# Search Views - form and visual 

@app.route('/searchbykeyword', methods=['GET'])
def search_term():
    """ Update visual to show new coverage for search term """

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_terms = user.searches
    else:
        user_terms = None

    return render_template('search_for_term.html',
                            user='user_id',
                            user_terms=user_terms)

@app.route('/topsearch.json', methods=['POST'])
def search_for_term():
    """ Update visual to show new coverage for search term """
    
    fav_search = request.form.get('favorite-search')
    keyword = request.form.get('keyword')
    add_or_remove = request.form.get('arterm')

    # if fav_search == None or fav_search == 'Search from Favorite Terms:':
    #     keyword = keyword
    if add_or_remove == 'favorite':
        user = User.query.get(session['user_id'])
        for search in user.searches: 
            if keyword == search.search_term:
                flash('You cannot favorite the same term twice!')
                return redirect('/searchbykeyword')
        else:
            term = Search.query.filter(Search.search_term == keyword).first()
            if term is None:
                term = Search(search_term=keyword)
            user.searches.append(term)
            db.session.commit()
            # flash('Your term is now added to favorites!')
    elif add_or_remove == 'delete':
        user = User.query.get(session['user_id'])
        term = Search.query.filter(Search.search_term == fav_search).one()
        user.searches.remove(term)
        db.session.commit()
            # flash('Your term is deleted')
    elif keyword == None or keyword == '' or keyword == []:
        keyword = fav_search
    
    r = requests.get(('https://newsapi.org/v2/top-headlines?language=en&q={}&sortBy=relevancy'+
                     '&apiKey=1ec5e2d27afa46efaf95cfb4c8938f37').format(keyword))

    top_search_json = r.json()

    # print top_search_json
    # print top_trending_json

    top_searches = top_search_json['articles']
    # # print top_articles

    # if top_searches == None:
    #     print 

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

# =============================================================================
# JSON routes for top and search coverage

@app.route('/toptrending.json')
def json_data():
    """Combine News API and database data"""

    r = requests.get("https://newsapi.org/v2/top-headlines?pageSize=30&sources=the-wall-street-journal,the-new-york-times,"+
                      "bbc-news,techcrunch,the-washington-post,cnn,fox-news,breitbart-news,time,wired,business-insider,"+
                      "politico,the-economist,reuters,cnbc,engadget,nbc-news,cbs-news,abc-news,fortune&apiKey=1ec5e2d27afa46efaf95cfb4c8938f37")
    #removed usa-today and daily
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

        #Need to remove popularity fom this part!!!
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

    user = User.query.filter(User.email == email).first()
    if user is None:
        flash('User not found')
        return redirect('/')

    if check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        flash('Logged in as {}'.format(user.email))
        return redirect('/')

    flash('Invalid password')
    return redirect('/')

    # users = User.query.all()
    # return render_template('login.html')

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

    if '@' or '.com' or '.edu' not in email:
        flash('Please enter a valid email address')
        return redirect('/register')
    elif len(password) > 8 and "1234567890" not in password:
        flash("Please enter a password with one or more numbers")
        return redirect('/register')

        hashed_value = generate_password_hash(password)

    if User.query.filter(User.email == email).first() is None:
        user = User(email=email, password=hashed_value)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        flash('Registered as {}'.format(email))
        return redirect('/')

    flash('User already exists - Please use different Email')
    return redirect('/register')

@app.route('/updateinfo', methods=['GET'])
def view_update_form():
    """ view form to update information """

    return render_template('update_account.html')

    
@app.route('/updateinfo', methods=['POST'])
def update_information():
    """ allow user to update password """

    email = request.form.get('email')
    new_password = request.form.get('password')

    user = User.query.filter(User.user_id == session['user_id']).one()

    # if email != '':
    #     user.email = new_email
    #     session['user_id'] = user.user_id
    if user.email == email: 
        if new_password != '':
            user.password = new_password
            flash('User password changed')
            return redirect('/')
    else:
        flash('You cannot change password for that account')
        return redirect('/')
    
    db.session.commit()


# =============================================================================
# User add outlet information


@app.route('/updateoutletinfo', methods=['GET'])
def view_update_outlet_form():
    """ view form to update outlet information """

    return render_template('update_outlet_information.html')
    
# @app.route('/updateoutletinfo', methods=['POST'])
# def update_outlet_information():
#     """ allow user to update outlet popularity or bias """

@app.route('/contact.php', methods=['POST'])
def email_update_outlet_form():

  flash('Thanks for submitting!')

  return redirect('/updateoutletinfo')

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