"""Flask Tests"""

import unittest
from server import app
from model import db, connect_to_db
from seed import example_data
from flask import session


class NewsflashTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        connect_to_db(app, "postgresql:///newsflashdb")
        self.client = app.test_client()

        with self.client as c:
          with c.session_transaction() as sess:
              sess['user_id'] = 1

    # def test_homepage(self):
    #     result = self.client.get("/")
    #     self.assertIn("Top Trending", result.data)

    def test_about(self):
        result = self.client.get("/aboutnewsflash")
        self.assertIn("NewsAPI", result.data)

    def test_register(self):
        result = self.client.get("/register")
        self.assertIn("Welcome to Newsflash!", result.data)

    def test_no_login_sign_up(self):
        if 'user_id' not in sess:
            result = self.client.get("/searchbykeyword")
            self.assertIn("Sign Up",result.data)
            self.assertNotIn("Manage Account", result.data)

    def test_favorite_search(self):
        result = self.client.get("/searchbykeyword")
        self.assertIn("Search", result.data)

    def test_fav_search_login(self):
        if 'user_id' in sess:
            result = self.client.get("/searchbykeyword")
            self.assertIn("Submit", result.data)

    # def test_register_works(self):
    #     result = self.client.post("/register",
    #                               data={"email": "chiggins@gmail.com",
    #                                     "password":"222222"},
    #                               follow_redirects=True)

    #     result.status_code == 200

    def test_login(self):
        result = self.client.post("/login",
                                  data={"email": "chiggins@lclark.edu"},
                                  follow_redirects=True)
        self.assertNotIn("Login",result.data)
        self.assertIn("Logout", result.data)

    def test_logout(self):
        result = self.client.post("/logout",
                                  data={"email": "chiggins@lclark.edu"},
                                  follow_redirects=True)

        self.assertNotIn("Loggout",result.data)
        self.assertIn("Login", result.data)

    def test_update_account_works(self):
        result = self.client.post("/update_account",
                                  follow_redirects=True)
        result.status_code == 200

    def _mock_keyword(keyword):
        return "Google"

        import server
        server.keyword = _mock_keyword

# class NewsflashTestDatabase(unittest.TestCase):
#     """Flask tests that use the database."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         # Connect to test database
#         connect_to_db(app, "postgresql:///newsflashdb")

#         # Create tables and add sample data
#         db.create_all()
#         example_data()

#     def tearDown(self):
#         """teardown"""

#         db.session.close()
#         db.drop_all()

#     def test_db(self):
#         if (user.email = "hellohellohello@gmail.com") and (search.search_term = "testestest") and (outlet.outlet_popularity = 10):
#             return True

if __name__ == "__main__":
    unittest.main()


