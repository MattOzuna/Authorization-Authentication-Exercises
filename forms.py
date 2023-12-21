from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField
from wtforms.validators import InputRequired

class AddRegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired()])
    
    password = PasswordField('Password',
                             validators=[InputRequired()])
    
    email = EmailField('email',
                            validators=[InputRequired()])
    
    first_name = StringField('First name',
                           validators=[InputRequired()])
    
    last_name = StringField('Last name',
                           validators=[InputRequired()])
    
    
class AddLoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired()])
    
    password = PasswordField('Password',
                             validators=[InputRequired()])
    
