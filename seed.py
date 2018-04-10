"""Seed Database"""

from sqlalchemy import func
from model import Outlet, User, Search, User_Search, connect_to_db, db
from server import app
from datetime import datetime

# =============================================================================

def load_users():
    """Load users into database from data in data folder"""

    print "Users"


    # for line in open(" "):
    #     line = line.rstrip().split(' ')

    

        db.session.add(user)

    db.session.commit()

def load_searches():
    """Load users into database from data in data folder"""

    print "Searches"


    # for line in open(" "):
    #     line = line.rstrip().split(' ')

    

        db.session.add(search)

    db.session.commit()

def load_outlets():
    """Load users into database from data in data folder"""

    print "Media Outlets"


    # for line in open("media_outlets.txt"):
    #     line = line.rstrip().split('|')


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
#     """Set value for the next movie_id after seeding database"""

#     result = db.session.query(func.max(Search.search_id)).one()
#     max_id = int(result[0])

#     query = "SELECT setval('searches_search_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()