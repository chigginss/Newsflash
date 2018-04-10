from flask_sqlalchemy import SQLAlchemy
import correlation
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

#many users can have many searches

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.users_id'),
                         nullable=False)

     users = db.relationship('User')
     searches = db.relationship('Search')

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


def example_data():
"""Sample test data for database."""

  user_1 = User(email="hello@gmail.com", password="1234")
  search_1 = Search(search_term="Google")
  outlet_1 = Outlet(name='Best News', outlet_popularity='10', outlet_bias='Leaning Conservative')

  db.session.add_all([user_1, search_1, outlet_1])
  db.session.commit()

