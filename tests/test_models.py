import unittest
from app import create_app, db
from app.models import User, Post

class ModelsTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary Flask application and in-memory database for testing."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        """Tear down the test database and application context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_user_model(self):
        """Test the User model for creation, password hashing, and password checking."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'  # This will hash the password
        db.session.add(user)
        db.session.commit()
        
        self.assertEqual(User.query.count(), 1)
        self.assertTrue(user.check_password('password123'))
        
    def test_post_model(self):
        """Test the Post model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()
        
        post = Post(title='Test Post', content='This is a test post', created_by=user.id)
        db.session.add(post)
        db.session.commit()
        
        self.assertEqual(Post.query.count(), 1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post')
        self.assertEqual(post.created_by, user.id)

if __name__ == '__main__':
    unittest.main()
