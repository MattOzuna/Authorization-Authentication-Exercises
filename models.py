from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    username = db.Column(db.Text,
                         nullable = False,
                         unique=True)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.Text,
                      nullable=False,
                      unique = True)
    
    first_name = db.Column(db.Text,
                          nullable=False)
    
    last_name = db.Column(db.Text,
                          nullable=False)