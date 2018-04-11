"""Flask Tests"""

import unittest

# from party import app
from model import db, connect_to_db
from seed import example_data


class NewsflashTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Homepage Test 1", result.data)

    def test_about(self):
        result = self.client.get("/about")
        self.assertIn("Tech Stack", result.data)

    def test_register(self):
        result = self.client.get("/register")
        self.assertIn("Welcome to Newsflash", result.data)

    def test_no_login_yet(self):
        result = self.client.get("/")
        self.assertIn("Login Here",result.data)
        self.assertNotIn("Logged In", result.data)

    # def test_favorite_search(self):
    #     result = self.client.get("/")
    #     self.assertIn("Google", result.data)

    def test_login(self):
        result = self.client.post("/login",
                                  data={"email": "chiggins@lclark.edu"},
                                  follow_redirects=True)

        self.assertNotIn("Login Here",result.data)
        self.assertIn("Logged In", result.data)

    def test_logout(self):
        result = self.client.post("/logout",
                                  data={"email": "chiggins@lclark.edu"},
                                  follow_redirects=True)

        self.assertNotIn("Logged In",result.data)
        self.assertIn("Logged Out", result.data)


class NewsflashTestDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        with self.client as c:
                with c.session_transaction() as sess:
                    sess['email'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///test1")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """teardown"""

        db.session.close()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()