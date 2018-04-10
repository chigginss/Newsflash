"""Seed Database"""

from sqlalchemy import func
from model import Outlet, User, Search, User_Search, connect_to_db, db
from server import app
from datetime import datetime

# =============================================================================

def load_users():
    """Load users into database from HTML form"""

    print "Users"

    email = request.form.get('email')
    password = request.form.get('password')

    user = User(email=email,
                password=password)

    db.session.add(user)

  db.session.commit()

def load_searches():
    """Load users into database from HTML form"""

    print "Searches"

    search_term = request.form.get('search')
      
    search = Search(search_term=search_term)

    db.session.add(search)

  db.session.commit()

def load_outlets():
    """Load outlet and information into database from data folder"""

    print "Media Outlets"


    for line in open("media_outlets.txt"):
        line = line.rstrip()
        name, popularity, bias = line.split('|')

    outlet =  Outlet(name=name,
                     popularity=popularity,
                     bias=bias)

    db.session.add(outlet)

  db.session.commit()

# def increment_user_id():
#     """Set value for the next user_id after seeding database"""

#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


# def increment_search_id():
#     """Set value for the next search_id after seeding database"""

#     result = db.session.query(func.max(Search.search_id)).one()
#     max_id = int(result[0])

#     query = "SELECT setval('searches_search_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()