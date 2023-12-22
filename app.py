from flask import Flask, render_template, flash, redirect, request, session
from models import db, connect_db, User, Feedback
from forms import AddRegisterForm, AddLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authorization"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

@app.route('/')
def rootRoute():
    return redirect('/register')


@app.route('/users/<username>')
def user_page(username):
    '''
    Secret page route requires a username to be in the flask session cookie.
    '''
    if session.get('username') == username:
        user = User.query.filter_by(username=username).one_or_404()
        feedback = user.feedback
        return render_template ('secret.html', user=user, feedback=feedback)
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
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Get route generates a form with WTF login form
    POST route takes the username and finds a user in the db that matches.
    If it is found, it check the password to see if it matches.
    If it matches the username is added to flask session and the user is redirected to secret route
    '''
    form = AddLoginForm()
    if form.validate_on_submit():
        user = User.validateUser(form)
        if user:
            session['username'] = form.username.data
            return redirect(f'/users/{user.username}')
        
        form.username.error = ['Invalid username/password']

    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username')
    flash('You are logged out')
    return redirect('/login')

@app.route('/users/<username>/delete', methods=['POST'])
def deleteUser(username):
    if not session.get('username'):
        flash('Please Login first')
        return redirect('/')
    if session.get('username') != username:
        flash('You can only view your Feedback')
        return redirect(f'/users/{session['username']}')
    
    user = User.query.filter_by(username=username).one_or_404()
    feedback = user.feedback
    db.session.delete(user)
    
    for feedback in feedback:
        db.session.delete(feedback)
    db.session.commit()

    session.pop('username')
    flash('Account deleted')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def addFeedback(username):
    '''
    On Get request, renders add feedback form
    On Post request, validates user is the correct user
    then add the feedback to the db and redirect back to users personal page
    '''

    # Making sure that only the user who is logged in can see this form
    if not session.get('username'):
        flash('Please Login first')
        return redirect('/')
    if session.get('username') != username:
        flash('You can only view your Feedback')
        return redirect(f'/users/{session['username']}')
    
    form = FeedbackForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        Feedback.addNewFeedback(form, user)
        return redirect(f'/users/{user.username}')
    
    return render_template('add-feedback.html', form=form)

@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def updateFeedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).one_or_404()
    username = feedback.user.username

    if not session.get('username'):
        flash('Please Login first')
        return redirect('/')
    if session.get('username') != username:
        flash('You can only edit your Feedback')
        return redirect(f'/users/{session['username']}')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        Feedback.updateFeedback(form, feedback)
        return redirect(f'/users/{username}')
    return render_template('update-feedback.html', form=form)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def deleteFeedback(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).one_or_404()
    username = feedback.user.username
    if not session.get('username'):
        # if they're not logged in
        flash('Please Login first')
        return redirect('/')
    if session.get('username') != username:
        # if they're trying to delete someone else feedback
        flash('You can only delete your Feedback')
        return redirect(f'/users/{session['username']}')
    
    db.session.delete(feedback)
    db.session.commit()
    
    return redirect(f'/users/{username}')


