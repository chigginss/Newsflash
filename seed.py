"""Seed Database"""

from sqlalchemy import func
from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime

# =============================================================================

def load_users():
    """Load users into database from data in data folder"""

    print "Article"


    for row in open("top_trending_articles"):
        row = row.rstrip().split(' ')

        title= 
        media_outlet = 
        date_published = datetime.strptime(, "%d-%b-%Y")
        url = 

        article = Article(title=title,
                      media_outlet=media_outlet,
                      author=author,
                      date_published=date_published,
                      url=url)

        db.session.add(article)

    db.session.commit()
