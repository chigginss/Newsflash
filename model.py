# from flask_sqlalchemy import SQLAlchemy
# import correlation
# import time

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

# db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Newsflash"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))
    
    searches = db.relationship('Search')

    def __repr__(self):
        """Representation of User instance"""

        return "<User: user_id={}, email={}>".format(self.user_id, self.email)

#many users can have many searches

class Search(db.Model):
    """Search by User on website."""

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_term = db.Column(db.String(64))

    users = db.relationship('User')

    def __repr__(self):
        """Representation of Search instance"""

        return "<Search: search_id={}, search_term={}>".format(self.search_id, self.search_term)

class Outlets(db.Model):
    """Adds popularity and bias values to outlet"""

    __tablename__ = "outlets"

    outlet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outlet_name = db.Column(db.String(64))
    outlet_popularity = db.Column(db.Integer)
    outlet_bias = db.Column(db.Integer)

    def __repr__(self):
        """Representation of Search instance"""

        return "<Outlet: outlet_id={}, outlet_name={}, outlet_popularity={}, outlet_bias={}>".format(self.outlet_id, self.outlet_name, self.outlet_popularity, self.outlet_bias)

class User_Search(db.Model):
    """ Tracks User Search """

    __tablename__ = "user_search"

    user_search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outlet_id = db.Column(db.Integer, db.ForeignKey('outlets.outlet_id'),
                         nullable=False)
    search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'),
                         nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'),
                         nullable=False)

     users = db.relationship('User')
     searches = db.relationship('Search')
     outlets = db.relationship('Outlet')

    def __repr__(self):
        """Representation of User instance"""

        return "<Outlet: user_search_id={}, outlet_id={}, search_id={}, user_id={}>".format(self.user_search_id, self.outlet_id, self.search_id, self.user_id)


