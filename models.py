"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
    
# deafult profile image is one is not entered by the user
default_url = 'https://t3.ftcdn.net/jpg/00/64/67/52/360_F_64675209_7ve2XQANuzuHjMZXP3aIYIpsDKEbF5dD.jpg'
    
    
class User(db.Model):
    # User model, adds columns for id, first name, last name and profile image
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25), nullable=False)
    
    last_name = db.Column(db.String(25), nullable=False)
    
    image_url = db.Column(db.String, nullable=False, default=default_url)
    
    posts = db.relationship("Post", backref="user")
    
    @property
    def full_name(self):
        # Adds first name and last name together 
        n = self
        return f'{n.first_name} {n.last_name}'
    
class Post(db.Model):
    #Post model, add columns or title, content, created_at(date and time) and a reference to user_id(rom the users table)
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(30), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'), 
                        nullable=False)
    
class PostTag(db.Model):
    
    __tablename__ = 'posts_tags'
    
    posts_id = db.Column(db.Integer,
                         db.ForeignKey('posts.id'),
                         primary_key=True)
    
    tags_id = db.Column(db.Integer,
                        db.ForeignKey('tags.id'),
                        primary_key=True)
    
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True,)
    
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    
    posts = db.relationship(
        'Post',
        secondary = 'posts_tags',
        backref = 'tags'
    )