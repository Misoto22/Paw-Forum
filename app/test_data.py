import sys
import os
from faker import Faker
from datetime import datetime

# Adjust the Python path to include the project root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import db, User, Post, Task, Reply, PostLike, ReplyLike, Activity
from app import create_app

# Initialize the app and database
app = create_app()
app.app_context().push()

# Initialize Faker
faker = Faker()

def delete_all_data():
    try:
        db.drop_all()
        db.create_all()
        print('All tables have been dropped and recreated.')
    except Exception as e:
        print(f'An error occurred: {e}')

def generate_users():
    users = []
    for _ in range(50):
        username = faker.unique.user_name()
        email = faker.unique.email()
        password = username  # Password same as username
        # Generate a random phone number with the australian phone number format
        phone = faker.numerify(text='04########')
        gender = faker.random_element(elements=('Male', 'Female', 'Other'))
        # Generate a random four digit postcode with the australian postcode format
        postcode = faker.numerify(text='####')
        pet_type = faker.random_element(elements=('Dog', 'Cat'))
        user_image = f'avatar{faker.random_int(min=1, max=24)}.png'

        user = User(
            username=username,
            email=email,
            password=password,
            phone=phone,
            gender=gender,
            postcode=postcode,
            join_at=datetime.utcnow(),
            pet_type=pet_type,
            user_image=user_image
        )
        users.append(user)
        db.session.add(user)

    db.session.commit()
    return users

def generate_posts(users):
    posts = []
    for i in range(1, 11):
        title = faker.sentence(nb_words=6)
        content = faker.paragraph(nb_sentences=5)
        category = faker.random_element(elements=('Daily', 'PetSitting', 'Adoption'))
        is_task = faker.boolean(chance_of_getting_true=25)
        created_by = faker.random_element(elements=users).id
        created_at = datetime.utcnow()
        like_count = faker.random_int(min=0, max=100)
        image_name = f'Image_{i}.png'  # Simulating image names

        post = Post(
            title=title,
            content=content,
            category=category,
            is_task=is_task,
            created_by=created_by,
            created_at=created_at,
            like_count=like_count,
            image_name=image_name
        )
        posts.append(post)
        db.session.add(post)

    db.session.commit()
    return posts

def generate_tasks(posts):
    for post in posts:
        if post.is_task:
            task = Task(
                id=post.id,
                status=faker.boolean(chance_of_getting_true=50),  # 50% chance of being True (open) or False (closed)
                assigned_to=None  # Initially, no user is assigned
            )
            db.session.add(task)

    db.session.commit()

def generate_replies(users, posts, n=50):
    replies = []
    # Generate base replies without parents
    for _ in range(n):
        post_id = faker.random_element(elements=posts).id
        reply_by = faker.random_element(elements=users).id
        content = faker.paragraph(nb_sentences=3)
        post_at = datetime.utcnow()
        like_count = faker.random_int(min=0, max=100)

        reply = Reply(
            post_id=post_id,
            reply_by=reply_by,
            content=content,
            post_at=post_at,
            like_count=like_count
        )
        replies.append(reply)
        db.session.add(reply)

    db.session.commit()

    # Generate child replies
    for _ in range(int(n / 2)):  # Let's say half of the replies will be child replies
        parent_reply = faker.random_element(elements=replies)
        post_id = parent_reply.post_id
        reply_by = faker.random_element(elements=users).id
        content = faker.paragraph(nb_sentences=3)
        post_at = datetime.utcnow()
        like_count = faker.random_int(min=0, max=100)

        child_reply = Reply(
            post_id=post_id,
            reply_by=reply_by,
            parent_reply_id=parent_reply.id,
            content=content,
            post_at=post_at,
            like_count=like_count
        )
        replies.append(child_reply)
        db.session.add(child_reply)

    db.session.commit()
    return replies

def generate_post_likes(users, posts):
    for post in posts:
        for _ in range(faker.random_int(min=0, max=10)):
            user = faker.random_element(elements=users)
            if not PostLike.query.filter_by(user_id=user.id, post_id=post.id).first():
                post_like = PostLike(
                    user_id=user.id,
                    post_id=post.id,
                    timestamp=datetime.utcnow()
                )
                db.session.add(post_like)
    db.session.commit()

def generate_reply_likes(users, replies):
    for reply in replies:
        for _ in range(faker.random_int(min=0, max=10)):
            user = faker.random_element(elements=users)
            if not ReplyLike.query.filter_by(user_id=user.id, reply_id=reply.id).first():
                reply_like = ReplyLike(
                    user_id=user.id,
                    reply_id=reply.id,
                    timestamp=datetime.utcnow()
                )
                db.session.add(reply_like)
    db.session.commit()

def generate_activities_for_user():
    user_id = 1
    target_user_id = faker.random_element([user.id for user in User.query.all() if user.id != user_id])
    actions = [
        "posted a new topic",
        "replied to a post",
        "liked a post",
        "liked a reply",
        "applied for a task",
        "posted a new topic",
        "replied to a post",
        "liked a post",
        "liked a reply",
        "applied for a task",
        "closed a task"
    ]
    for _ in range(10):
        action = faker.random_element(actions)
        activity = Activity(
            user_id=user_id,
            action=action,
            target_user_id=target_user_id if "liked" in action else None,
            timestamp=datetime.utcnow()
        )
        db.session.add(activity)
    db.session.commit()

def delete_all_activities():
    try:
        num_rows_deleted = db.session.query(Activity).delete()
        db.session.commit()
        print(f"Deleted {num_rows_deleted} rows from the Activity table.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Generate data
    users = generate_users()
    posts = generate_posts(users)
    generate_tasks(posts)
    replies = generate_replies(users, posts, n=50)
    generate_post_likes(users, posts)
    generate_reply_likes(users, replies)
    generate_activities_for_user()
    print('Test data generated successfully!')
