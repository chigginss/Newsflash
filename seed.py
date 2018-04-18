"""Seed Database"""

from sqlalchemy import func
from model import Outlet, User, Search, User_Search, connect_to_db, db
from server import app
from datetime import datetime

# =============================================================================

def example_data():
    """Sample test data for database."""

    user_1 = User(email="hello@gmail.com", password="1234")
    search_1 = Search(search_term="Google")
    outlet_1 = Outlet(outlet_name='Best News', outlet_popularity=10, outlet_bias='Right-Center')
    user_search_1 = User_Search(user_id=1, search_id=1)

    db.session.add_all([user_1, search_1, outlet_1])
    db.session.commit()

def load_outlets():
    """Load outlet and information into database from data folder"""

    for line in open("Data/media_outlets.txt"):
        line = line.rstrip()
        name, popularity, bias, _ = line.split('|')

        if popularity == 'NULL': 
            popularity = None
        else:
            popularity == int(popularity)

        if bias == 'NULL':
            bias = None

        outlet = Outlet(outlet_name=name,
                        outlet_popularity=popularity,
                        outlet_bias=bias)

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

if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    example_data()
    load_outlets()
    print "Connected to DB."