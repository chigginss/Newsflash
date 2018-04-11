from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User of Newsflash"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    searches = db.relationship("Search",
                            secondary = "user_searches",
                            backref="users")

    def __repr__(self):
        """Representation of User instance"""

        return "<User: user_id={}, email={}>".format(self.user_id, self.email)


class Search(db.Model):
    """Search by User on website."""

    __tablename__ = "searches"

    search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    search_term = db.Column(db.String(64))

    def __repr__(self):
        """Representation of Search instance"""

        return "<Search: search_id={}, search_term={}>".format(self.search_id, self.search_term)

class User_Search(db.Model):
    """ Tracks User Search """

    __tablename__ = "user_searches"

    user_search_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    search_id = db.Column(db.Integer, db.ForeignKey('searches.search_id'),
                         nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                         nullable=False)

    def __repr__(self):
        """Representation of User instance"""

        return "<Outlet: user_search_id={}, search_id={}, user_id={}>".format(self.user_search_id, self.search_id, self.user_id)

class Outlet(db.Model):
    """Adds popularity and bias values to outlet"""

    __tablename__ = "outlets"

    outlet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    outlet_name = db.Column(db.String(64))
    outlet_popularity = db.Column(db.Integer)
    outlet_bias = db.Column(db.String(64))

    def __repr__(self):
        """Representation of Search instance"""

        return "<Outlet: outlet_id={}, outlet_name={}, outlet_popularity={}, outlet_bias={}>".format(self.outlet_id, self.outlet_name, self.outlet_popularity, self.outlet_bias)

##############################################################################
# Model definitions

def connect_to_db(app, db_url='postgresql:///test1'):
    """ Connect database to Flask app"""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."

