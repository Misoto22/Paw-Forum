import unittest
from app import create_app, db
from app.models import User, Post

class RoutesTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary Flask application and in-memory database for testing routes."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        # Create a test user for authentication-related tests
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.password = 'password123'
        db.session.add(self.test_user)
        db.session.commit()
        
    def tearDown(self):
        """Tear down the test database and application context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Test the home page route for a successful response."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Paw Forum', response.data)

    def test_signup_positive(self):
        """Test the signup route for a successful registration."""
        response = self.client.post('/signup', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)

    def test_signup_negative_existing_user(self):
        """Test the signup route for a duplicate user registration failure."""
        response = self.client.post('/signup', data=dict(
            username='testuser',
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username or Email already exists', response.data)

    def test_signup_edge_case_empty_fields(self):
        """Test the signup route with empty fields."""
        response = self.client.post('/signup', data=dict(
            username='',
            email='',
            password=''
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All fields are required', response.data)

    def test_signup_invalid_email(self):
        """Test the signup route with invalid email format."""
        response = self.client.post('/signup', data=dict(
            username='newuser',
            email='invalid-email',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email format', response.data)

    def test_login_positive(self):
        """Test the login route for a successful login."""
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_negative_wrong_password(self):
        """Test the login route with an incorrect password."""
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_login_negative_nonexistent_user(self):
        """Test the login route with a nonexistent user."""
        response = self.client.post('/login', data=dict(
            username='nonexistent',
            password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout_positive(self):
        """Test the logout route for a successful logout."""
        # First, log in the test user
        self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        
        # Then, log out
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)

    def test_reply_requires_login(self):
        """Test that the reply route requires login."""
        response = self.client.get('/reply', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_reply_authenticated(self):
        """Test accessing the reply route when authenticated."""
        self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        response = self.client.get('/reply')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reply', response.data)

    def test_users_page(self):
        """Test the users page route for a successful response."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Users', response.data)

    def test_profile_page(self):
        """Test the profile page route for a successful response."""
        self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile', response.data)

    def test_post_create_page_requires_login(self):
        """Test that the post create page requires login."""
        response = self.client.get('/postcreate', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page.', response.data)

    def test_post_create_page_authenticated(self):
        """Test accessing the post create page when authenticated."""
        self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        response = self.client.get('/postcreate')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PostCreate', response.data)

    def test_search(self):
        """Test the search route with a query."""
        self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        post = Post(title='Test Post', content='This is a test post', created_by=self.test_user.id)
        db.session.add(post)
        db.session.commit()
        response = self.client.get('/search?query=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_search_no_query(self):
        """Test the search route with no query."""
        self.client.post('/login', data=dict(
            username='testuser',
            password='password123'
        ), follow_redirects=True)
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Posts found', response.data)

    def test_404_error(self):
        """Test the 404 error handling."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)

    def test_500_error(self):
        """Test the 500 error handling by causing an intentional error."""
        with self.assertRaises(Exception):
            response = self.client.get('/cause_500', follow_redirects=True)
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'Internal Server Error', response.data)

if __name__ == '__main__':
    unittest.main()
