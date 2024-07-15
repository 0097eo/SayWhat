# models.py

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='author', cascade='all, delete-orphan')

    

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username must be provided.")
        return username

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address.")
        return email

    serialize_rules = ('-_password_hash',)

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post title must be provided.")
        return title

    serialize_rules = ('-author.posts', '-comments.post')

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='comments')

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    post = db.relationship('Post', back_populates='comments')

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Comment content must be provided.")
        return content

    serialize_rules = ('-author.comments', '-post.comments')