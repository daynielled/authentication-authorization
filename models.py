from flask_sqlalchemy import SQLAlchemy, backref
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site User"""
        
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    username = db.Column(db.Text(20),nullable=False,unique=True)

    password = db.Column(db.Text,nullable=False)
    
    email = db.Column(db.Text (50),nullable=False,unique=True)

    first_name = db.Column(db.Text(30),nullable=False)
    
    last_name = db.Column(db.Text(30),nullable=False)
    

class Feedback(db.Model):
    """Feedback"""

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    user_username = db.Column(db.Text, db.ForeignKey('user.username'), nullable=False)

    user = db.relationship('User', backref=backref('feedbacks', lazy=True))    
    

         
    db.create_all()