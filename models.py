from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

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
    
    @classmethod
    def addNewUser(cls, form):
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        utf8_password = hashed_password.decode('utf8')

        return cls(username=username,
                   password=utf8_password,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)
    
    @classmethod
    def validateUser(cls, form):
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        
        return False