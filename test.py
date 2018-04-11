"""Flask Tests"""

import unittest
from server import app
from model import db, connect_to_db
from seed import example_data
# import flask


class NewsflashTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "postgresql:///test1")

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Homepage Test 1", result.data)

    def test_about(self):
        result = self.client.get("/aboutnewsflash")
        self.assertIn("NEED LOGOS", result.data)

    def test_register(self):
        result = self.client.get("/register")
        self.assertIn("Welcome to Newsflash!", result.data)

    def test_no_login_yet(self):
        result = self.client.get("/")
        self.assertIn("Login",result.data)
        self.assertNotIn("Logout", result.data)

    def test_favorite_search(self):
        result = self.client.get("/newsbykeyword")
        self.assertIn("Search to Favorite", result.data)

    def test_register_works(self):
        result = self.client.post("/register",
                                  data={"email": "jane@jane.com",
                                        "password":"2222"},
                                  follow_redirects=True)
        # import pdb; pdb.set_trace()
        result.status_code == 200

# class NewsflashTestDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         self.client = app.test_client()
#         app.config['TESTING'] = True
#         with self.client as c:
#                 with c.session_transaction() as sess:
#                     sess['email'] = True

#         # Connect to test database
#         connect_to_db(app, "postgresql:///test1")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """teardown"""

#         db.session.close()
#         db.drop_all()

#     def test_db(self):
#         """Test departments page."""

#         result = self.client.get("/users")
#         self.assertIn("chiggins@lclark.edu", result.data)

if __name__ == "__main__":
    unittest.main()

# =============================================================================
# TESTS TO ADD !!!!!!!!!!!!!!!!!!!!!!!!!!

#MOCKING - fake db to test for email in session for both login and logout##
    # def test_login(self):
    #     result = self.client.post("/login",
    #                               data={"email": "chiggins@lclark.edu"},
    #                               follow_redirects=True)
    #     self.assertNotIn("Login",result.data)
    #     self.assertIn("Logout", result.data)

    # def test_logout(self):
    #     result = self.client.post("/logout",
    #                               data={"email": "chiggins@lclark.edu"},
    #                               follow_redirects=True)

    #     self.assertNotIn("Logged In",result.data)
    #     self.assertIn("Logged Out", result.data)
#API TEST ======================================================================

# def _mock_get_trending_articles('https://newsapi.org/v2/top-headlines?language=en&sources=google-news&apiKey={}'.format(API_KEY)')):
#     return for article in data['articles']:
#         description = (article['description'] or " ").encode('utf-8')
#         title = (article['title'] or " ").encode('utf-8')
#         url = (article['url'] or " ").encode('utf-8')
#         author = (article['author'] or " ").encode('utf-8') 
#         publishedAt = (article['publishedAt'] or " ").encode('utf-8')
#         source = (article['source']['name'] or " ").encode('utf-8')
#         urlToImage = (article['urlToImage'] or " ").encode('utf-8')
# import server
# server.get_trending_articles = _mock_get_trending_articles

# def setUp(self):

#     def _mock_get_trending_articles('https://newsapi.org/v2/top-headlines?language=en&sources=google-news&apiKey={}'.format(API_KEY))'
#         return for article in data['articles']:
#         description = (article['description'] or " ").encode('utf-8')
#         title = (article['title'] or " ").encode('utf-8')
#         url = (article['url'] or " ").encode('utf-8')
#         author = (article['author'] or " ").encode('utf-8') 
#         publishedAt = (article['publishedAt'] or " ").encode('utf-8')
#         source = (article['source']['name'] or " ").encode('utf-8')
# server.get_trending_articles = _mock_get_trending_articles

