import unittest
from app import create_app, db
from app.models import User, Post
from sqlalchemy.exc import IntegrityError
from app.config import TestingConfig

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank database before each test."""
        self.app = create_app(TestingConfig)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the test database and application context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model_creation(self):
        """Test the User model for creation, password hashing, and password checking."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'  # This will hash the password
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.count(), 1)
        self.assertTrue(user.check_password('password123'))

    def test_user_model_unique_username(self):
        """Test that the username is unique in the User model."""
        user1 = User(username='testuser', email='test1@example.com')
        user1.password = 'password123'
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='testuser', email='test2@example.com')
        user2.password = 'password456'
        db.session.add(user2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_model_unique_email(self):
        """Test that the email is unique in the User model."""
        user1 = User(username='testuser1', email='test@example.com')
        user1.password = 'password123'
        db.session.add(user1)
        db.session.commit()

        user2 = User(username='testuser2', email='test@example.com')
        user2.password = 'password456'
        db.session.add(user2)

        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_user_model_invalid_email(self):
        """Test that an invalid email raises an error."""
        with self.assertRaises(ValueError):
            user = User(username='testuser', email='invalid-email')
            db.session.add(user)
            db.session.commit()

    def test_post_model_creation(self):
        """Test the Post model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='This is a test content', created_by=user.id)
        db.session.add(post)
        db.session.commit()

        self.assertEqual(Post.query.count(), 1)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test content')
        self.assertEqual(post.created_by, user.id)

    def test_post_model_empty_title(self):
        """Test that creating a Post with an empty title raises an error."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        with self.assertRaises(ValueError):
            post = Post(title='', content='This is a test content', created_by=user.id)
            db.session.add(post)
            db.session.commit()

    def test_post_model_long_title(self):
        """Test that creating a Post with a very long title raises an error."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        long_title = 'a' * 201  # Title exceeds 200 characters
        with self.assertRaises(ValueError):
            post = Post(title=long_title, content='This is a test content', created_by=user.id)
            db.session.add(post)
            db.session.commit()


    def test_post_model_null_content(self):
        """Test that creating a Post with null content raises an error."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        with self.assertRaises(ValueError):
            post = Post(title='Test Post', content=None, created_by=user.id)
            db.session.add(post)
            db.session.commit()


    def test_post_model_no_user(self):
        """Test that creating a Post without a user raises an error."""
        with self.assertRaises(IntegrityError):
            post = Post(title='Test Post', content='This is a test content', created_by=None)
            db.session.add(post)
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
