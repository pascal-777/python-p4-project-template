#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Channel, Blog, Comment, UserChannel


def seed_data():
    fake = Faker()
    with app.app_context():
        #drop all table if exist
        print("Starting drop...")
        db.drop_all()
        db.create_all()
        print("Starting seed...")

        users = []
        for _ in range(50):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password="password",
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()


        blogs = []
        for _ in range(100):
            blog = Blog(
                title=fake.sentence(),
                content=fake.paragraph(),
                topic=rc(["python", "django", "flask", 'react', 'vue', 'angular']),
                user_id=rc(users).id,
                channel_id=rc(users).id
            )
            blogs.append(blog)
        db.session.add_all(blogs)
        db.session.commit()

        comments = []
        for _ in range(100):
            comment = Comment(
                body=fake.paragraph(),
                user_id=rc(users).id,
                blog_id=rc(blogs).id
            )
            comments.append(comment)
        db.session.add_all(comments)
        db.session.commit()

        channels = []
        for _ in range(10):
            channel = Channel(
                channel_name=fake.word(),
                creator_id=rc(users).id,
                owner=rc(users).username
            )
            channels.append(channel)
        db.session.add_all(channels)
        db.session.commit()

        user_channels = []
        for _ in range(50):
            user_channel = UserChannel(
                user_id=rc(users).id,
                channel_id=rc(channels).id
            )
            user_channels.append(user_channel)
        db.session.add_all(user_channels)
        db.session.commit()
        # Seed code goes here!
        print("complete seeding!")

if __name__ == '__main__':
    seed_data()
