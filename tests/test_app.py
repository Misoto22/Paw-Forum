import unittest
from flask import Flask
from app import create_app, db
from app.models import User

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test environment. Create an instance of the app with testing configuration,
        initialize the database, and create a test client.
        """
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
    def tearDown(self):
        """
        Tear down the test environment. Remove the database session and drop all tables.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """
        Test the home page. Ensure it loads correctly and contains the expected content.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Paw Forum', response.data)

    def test_signup(self):
        """
        Test the signup functionality. Ensure a user can sign up successfully,
        and verify the user is added to the database.
        """
        response = self.client.post('/signup', data=dict(
            username='testuser',
            email='test@example.com',
            password='password123',
            phone='1234567890',
            gender='Male',
            postcode='12345'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)

    def test_login(self):
        """
        Test the login functionality. Ensure a user can log in successfully
        and verify the correct response.
        """
        # Create a test user
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_logout(self):
        """
        Test the logout functionality. Ensure a user can log out successfully
        and verify the correct response.
        """
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)

if __name__ == '__main__':
    unittest.main()
