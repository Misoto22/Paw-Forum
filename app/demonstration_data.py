import sys
import os
from faker import Faker
from datetime import datetime
from werkzeug.utils import secure_filename
import shutil
from werkzeug.security import generate_password_hash
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import db, User, Post, Task, Reply, PostLike, ReplyLike, Activity, WaitingList
from app import create_app

PET_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'image', 'sample')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'image', 'uploads')


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
    for _ in range(20):
        while True:
            username = faker.unique.user_name()
            if len(username) >= 10:
                break
        email = faker.unique.email()
        password = username
        phone = faker.numerify(text='04########')
        gender = faker.random_element(elements=('Male', 'Female', 'Other'))
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

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_posts(users, source_image_folder, upload_folder):
    posts = []
    image_files = [f for f in os.listdir(source_image_folder) if allowed_file(f)]

    if not image_files:
        raise ValueError("No valid image files found in the source image folder.")

    for i in range(1, 61):  # Creating posts
        title = faker.sentence(nb_words=6)
        content = faker.paragraph(nb_sentences=5)
        category = faker.random_element(elements=('Daily', 'PetSitting', 'Adoption'))
        is_task = faker.boolean(chance_of_getting_true=25)
        created_by = faker.random_element(elements=users).id
        created_at = faker.date_time_this_year()
        like_count = faker.random_int(min=0, max=100)
        
        # Select a random image from the source folder
        selected_image = faker.random_element(elements=image_files)
        original_filename = secure_filename(selected_image)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4()}.{file_ext}"
        image_path = os.path.join(upload_folder, new_filename)
        
        # Copy the image to the upload folder with the new name
        shutil.copy(os.path.join(source_image_folder, selected_image), image_path)

        post = Post(
            title=title,
            content=content,
            category=category,
            is_task=is_task,
            created_by=created_by,
            created_at=created_at,
            like_count=like_count,
            image_name=new_filename  # Save the new image name to the post
        )
        posts.append(post)
        db.session.add(post)

    db.session.commit()
    return posts
def generate_tasks(posts):
    tasks = []
    for post in posts:
        if post.is_task:
            task = Task(
                id=post.id,
                status=faker.boolean(chance_of_getting_true=50),
                assigned_to=None
            )
            tasks.append(task)
            db.session.add(task)
    db.session.commit()
    return tasks

def generate_waiting_list_entries(users, tasks):
    waiting_list_entries = []
    for task in tasks:
        num_entries = faker.random_int(min=0, max=10)
        for _ in range(num_entries):
            user = faker.random_element(elements=users)
            # Check if the user already applied for this task
            existing_entry = WaitingList.query.filter_by(task_id=task.id, user_id=user.id).first()
            if not existing_entry:
                waiting_list_entry = WaitingList(
                    task_id=task.id,
                    user_id=user.id,
                    applied_at=faker.date_time_this_year()
                )
                waiting_list_entries.append(waiting_list_entry)
                db.session.add(waiting_list_entry)
    db.session.commit()
    return waiting_list_entries

def generate_replies(users, posts, n=600):
    replies = []

    # Generate base replies without parents
    for _ in range(int(n * 0.7)):  # 70% base replies
        post_id = faker.random_element(elements=posts).id
        reply_by = faker.random_element(elements=users).id
        content = faker.paragraph(nb_sentences=3)
        post_at = faker.date_time_this_year()
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
    for _ in range(int(n * 0.3)):  # 30% child replies
        parent_reply = faker.random_element(elements=replies)
        post_id = parent_reply.post_id
        reply_by = faker.random_element(elements=users).id
        content = faker.paragraph(nb_sentences=3)
        post_at = faker.date_time_this_year()
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

def generate_replies(users, posts, n=500):
    replies = []

    # Generate base replies without parents
    for _ in range(int(n * 0.7)):  # 70% base replies
        post_id = faker.random_element(elements=posts).id
        reply_by = faker.random_element(elements=users).id
        content = faker.paragraph(nb_sentences=3)
        post_at = faker.date_time_this_year()
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
    for _ in range(int(n * 0.3)):  # 30% child replies
        parent_reply = faker.random_element(elements=replies)
        post_id = parent_reply.post_id
        reply_by = faker.random_element(elements=users).id
        content = faker.paragraph(nb_sentences=3)
        post_at = faker.date_time_this_year()
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
        for _ in range(faker.random_int(min=0, max=70)):
            user = faker.random_element(elements=users)
            if not PostLike.query.filter_by(user_id=user.id, post_id=post.id).first():
                post_like = PostLike(
                    user_id=user.id,
                    post_id=post.id,
                    timestamp=faker.date_time_this_year()
                )
                db.session.add(post_like)
    db.session.commit()

def generate_reply_likes(users, replies):
    for reply in replies:
        for _ in range(faker.random_int(min=0, max=30)):
            user = faker.random_element(elements=users)
            if not ReplyLike.query.filter_by(user_id=user.id, reply_id=reply.id).first():
                reply_like = ReplyLike(
                    user_id=user.id,
                    reply_id=reply.id,
                    timestamp=faker.date_time_this_year()
                )
                db.session.add(reply_like)
    db.session.commit()

def generate_activities(users):
    actions_with_target = [
        "replied to a post of",
        "deleted a reply to",
        "liked a post from",
        "liked a reply from",
        "unliked a post from",
        "unliked a reply from",
        "applied a task from"
    ]
    actions_without_target = [
        "updated profile!",
        "created a post.",
        "deleted a post.",
        "closed your task."
    ]

    for user in users:
        for _ in range(faker.random_int(min=5, max=50)):
            if faker.boolean(chance_of_getting_true=50):
                action = faker.random_element(actions_with_target)
                target_user_id = faker.random_element([u.id for u in users if u.id != user.id])
                target_user = db.session.get(User, target_user_id)
                action_description = f"{action} {target_user.username}"
            else:
                action = faker.random_element(actions_without_target)
                target_user_id = None
                action_description = action

            activity = Activity(
                user_id=user.id,
                action=action_description,
                target_user_id=target_user_id,
                timestamp=faker.date_time_this_year()
            )
            db.session.add(activity)
    db.session.commit()

if __name__ == '__main__':
    delete_all_data()
    users = generate_users()
    posts = generate_posts(users, PET_FOLDER, UPLOAD_FOLDER)
    tasks = generate_tasks(posts)
    generate_waiting_list_entries(users, tasks)
    replies = generate_replies(users, posts, n=500)
    generate_post_likes(users, posts)
    generate_reply_likes(users, replies)
    generate_activities(users)
    print('Test data generated successfully!')
