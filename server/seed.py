# seed.py

from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta

from app import app
from models import db, User, Post, Comment

fake = Faker()

def create_fake_users(num_users=10):
    users = []
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.password_hash = fake.password()
        users.append(user)
    return users

def create_fake_posts(users, num_posts=50):
    posts = []
    for _ in range(num_posts):
        post = Post(
            title=fake.sentence(),
            content='\n\n'.join(fake.paragraphs(nb=3)),  # Join paragraphs into a single string
            author=choice(users),
            created_at=fake.date_time_between(start_date='-1y', end_date='now'),
        )
        posts.append(post)
    return posts

def create_fake_comments(users, posts, num_comments=100):
    comments = []
    for _ in range(num_comments):
        comment = Comment(
            content=fake.paragraph(),
            author=choice(users),
            post=choice(posts),
            created_at=fake.date_time_between(start_date='-1y', end_date='now'),
        )
        comments.append(comment)
    return comments

def seed_database():
    print("Seeding database...")
    
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create fake data
    users = create_fake_users()
    db.session.add_all(users)
    db.session.commit()

    posts = create_fake_posts(users)
    db.session.add_all(posts)
    db.session.commit()

    comments = create_fake_comments(users, posts)
    db.session.add_all(comments)
    db.session.commit()

    print("Seeding completed!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()