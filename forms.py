from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length

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
    
    
class FeedbackForm(FlaskForm):
    title = StringField('Title',
                        validators=[InputRequired(),
                                    Length(max=100,
                                           message='Cannot be over 100 characters')])

    content = TextAreaField('Content',
                          validators=[InputRequired()])