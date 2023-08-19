from flask_testing import TestCase

from backend.src.database import db
from backend.tests.tests_main import create_test_app


class SessionTests(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        return create_test_app(self)

    def test_simple_registration(self):
        response = self.client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})
        self.assertEquals(response.json, dict(message='registered successfully'))

    def test_dont_allow_duplicate_registrations(self):
        self.client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})
        response = self.client.post("/register", json={"username": "user1", 'password': 'pass1', 'email': 'email1'})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json, dict(error='user already exists'))
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
