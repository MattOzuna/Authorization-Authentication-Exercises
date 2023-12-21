from flask import Flask, render_template, flash, redirect, request, session
from models import db, connect_db, User 
from forms import AddRegisterForm, AddLoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authorization"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

@app.route('/')
def rootRoute():
    return redirect('/register')

@app.route('/secret')
def secret_page():
    '''
    Secret page route requires a username to be in the flask session cookie.
    '''

    if 'username' in session:
        return render_template ('secret.html')
    flash('Login first!')
    return redirect('/login')



@app.route('/register', methods=['GET', 'POST'])
def registration():
    '''
    GET route generates a form with WTF login form
    POST route receives form data and adds to db
    if username or email are taken is taken redirects to
    '''
    form = AddRegisterForm()

    if form.validate_on_submit():
        new_user = User.addNewUser(form)
        db.session.add(new_user)
        try:
            # this is to check and see if the unique constraints are met
            db.session.commit()

        except IntegrityError:
            flash('username/email already in use')
            return redirect('/register')
        
        session['username'] = form.username.data
        flash('Account Created!')
        return redirect('/secret')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AddLoginForm()
    if form.validate_on_submit():
        user = User.validateUser(form)
        if user:
            session['username'] = form.username.data
            return redirect('/secret')
        
        form.username.error = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop['username']
    flash('You are logged out')
    return redirect('/')

