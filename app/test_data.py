from faker import Faker
from datetime import datetime
from app.models import db, User, Post, Task, Reply
from app import create_app

# Initialize the app and database
app = create_app()
app.app_context().push()

# Initialize Faker
faker = Faker()

def generate_users():
    users = []
    for _ in range(3):
        username = faker.unique.user_name()
        email = faker.unique.email()
        password = username  # Password same as username
        phone = faker.phone_number()
        gender = faker.random_element(elements=('Male', 'Female', 'Other'))
        postcode = faker.postcode()
        pet_type = faker.random_element(elements=('Cat', 'Dog', 'Fish', 'Bird', 'Rabbit', 'Other'))
        user_image = f'/static/image/avatar/avatar{faker.random_int(min=1, max=32)}.png'

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
        category = faker.random_element(elements=('Daily', 'Petsitting', 'Adoption'))
        is_task = faker.boolean(chance_of_getting_true=25)
        created_by = faker.random_element(elements=users).id
        created_at = datetime.utcnow()
        image_path = f'/static/uploads/{i}'

        post = Post(
            title=title,
            content=content,
            category=category,
            is_task=is_task,
            created_by=created_by,
            created_at=created_at,
            image_path=image_path
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
                status=faker.random_element(elements=('open', 'closed')),
                assigned_to=None  # Initially, no user is assigned
            )
            db.session.add(task)

    db.session.commit()

def generate_replies(users, posts, n=50):
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
        db.session.add(reply)

    db.session.commit()

if __name__ == '__main__':
    # Generate data
    users = generate_users()
    posts = generate_posts(users)
    generate_tasks(posts)
    generate_replies(users, posts, n=50)
    print('Test data generated successfully!')
