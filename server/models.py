from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from config import db
from datetime import datetime
#add validations(email validation, phone number validation), password hashing(use bcrypt), 


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    secondary_email = db.Column(db.String(255))
    profile_pic = db.Column(db.LargeBinary)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    dob = db.Column(db.DateTime)
    phone_number = db.Column(db.String(10), unique=True)  # Adjusted to varchar to handle phone numbers properly
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    blogs = db.relationship('Blog', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    channels_created = db.relationship('Channel', backref='creator', lazy=True)
    user_channels = db.relationship('UserChannel', backref='user', lazy=True)
    

    serialize_rules = (
        '-id',
        '-password',
        '-blogs',
        '-comments',
        '-channels_created',
        '-user_channels'
    )

class Blog(db.Model, SerializerMixin):
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', backref='blog', lazy=True)

    serialize_rules = (
        '-id',
        '-user_id',
        '-channel_id',
        '-comments'
    )

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_rules = (
        '-id',
        '-user_id',
        '-blog_id'
    )

class Channel(db.Model, SerializerMixin):
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(255), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Adjusted foreign key reference
    owner = db.Column(db.String(255), nullable=False)

    blogs = db.relationship('Blog', backref='channel', lazy=True)
    user_channels = db.relationship('UserChannel', backref='channel', lazy=True)
    

    serialize_rules = (
        '-id',
        '-creator_id',
        '-blogs',
        '-user_channels'
    )

class UserChannel(db.Model, SerializerMixin):
    __tablename__ = 'user_channel'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)

    serialize_rules = (
        '-id',
        '-user_id',
        '-channel_id'
    )
