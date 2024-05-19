import unittest
from app import create_app, db
from app.models import User, Post, Task, WaitingList, Reply, PostLike, ReplyLike
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

    def test_task_model_creation(self):
        """Test the Task model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Task Post', content='This is a test task content', created_by=user.id, is_task=True)
        db.session.add(post)
        db.session.commit()

        task = Task(id=post.id, status=True, assigned_to=user.id)
        db.session.add(task)
        db.session.commit()

        self.assertEqual(Task.query.count(), 1)
        self.assertTrue(task.status)
        self.assertEqual(task.assigned_to, user.id)

    def test_reply_model_creation(self):
        """Test the Reply model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='This is a test content', created_by=user.id)
        db.session.add(post)
        db.session.commit()

        reply = Reply(post_id=post.id, reply_by=user.id, content='This is a test reply content')
        db.session.add(reply)
        db.session.commit()

        self.assertEqual(Reply.query.count(), 1)
        self.assertEqual(reply.content, 'This is a test reply content')
        self.assertEqual(reply.post_id, post.id)
        self.assertEqual(reply.reply_by, user.id)

    def test_waiting_list_model_creation(self):
        """Test the WaitingList model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Task Post', content='This is a test task content', created_by=user.id, is_task=True)
        db.session.add(post)
        db.session.commit()

        waiting_list_entry = WaitingList(task_id=post.id, user_id=user.id)
        db.session.add(waiting_list_entry)
        db.session.commit()

        self.assertEqual(WaitingList.query.count(), 1)
        self.assertEqual(waiting_list_entry.task_id, post.id)
        self.assertEqual(waiting_list_entry.user_id, user.id)

    def test_post_like_model_creation(self):
        """Test the PostLike model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='This is a test content', created_by=user.id)
        db.session.add(post)
        db.session.commit()

        post_like = PostLike(user_id=user.id, post_id=post.id)
        db.session.add(post_like)
        db.session.commit()

        self.assertEqual(PostLike.query.count(), 1)
        self.assertEqual(post_like.user_id, user.id)
        self.assertEqual(post_like.post_id, post.id)

    def test_reply_like_model_creation(self):
        """Test the ReplyLike model for creation and attribute assignment."""
        user = User(username='testuser', email='test@example.com')
        user.password = 'password123'
        db.session.add(user)
        db.session.commit()

        post = Post(title='Test Post', content='This is a test content', created_by=user.id)
        db.session.add(post)
        db.session.commit()

        reply = Reply(post_id=post.id, reply_by=user.id, content='This is a test reply content')
        db.session.add(reply)
        db.session.commit()

        reply_like = ReplyLike(user_id=user.id, reply_id=reply.id)
        db.session.add(reply_like)
        db.session.commit()

        self.assertEqual(ReplyLike.query.count(), 1)
        self.assertEqual(reply_like.user_id, user.id)
        self.assertEqual(reply_like.reply_id, reply.id)


if __name__ == '__main__':
    unittest.main()
