
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import db
from app import DatabaseManager
from app.forms import RegistrationForm
from app.forms import LoginForm
from app.forms import TopicForm
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/home')
def home():
    ## Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## Create a login and registration FlaskForm
    loginForm = LoginForm()
    regForm = RegistrationForm()
    ## Pass created forms into template
    return render_template('home.html', title="munapp", loginForm=loginForm, regForm=regForm)

@app.route('/register', methods=['GET', 'POST'])
def register():
    ## Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## Create FlaskForm child object defined in forms.py
    form = RegistrationForm()
    ## Checks if request is POST request and validates form This also checks
    ## for duplicate usernames/emails and matching password fields
    if form.validate_on_submit():
        ## Create new user and add to database
        DatabaseManager.addUser(form.username.data, form.email.data, \
        form.password.data)
        return redirect(url_for('login'))
    ## If form isn't valid we send user back to registration page
    ## and display correct error messages
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    ## Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## Create FlaskForm child object defined in forms.py
    form = LoginForm()
    if form.validate_on_submit():
        ## Check user submitted information with database via DatabaseManager
        ## and if correct log in user under account matching that information
        return DatabaseManager.login(form.username.data, form.password.data, \
        form.remember_me.data)
    ## If information does not match any accounts, return user to login page
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    return DatabaseManager.logout();

@app.route('/index')
@login_required
def index():
    users = DatabaseManager.getAllUsers()
    topics = DatabaseManager.getAllTopics()
    comments = DatabaseManager.getAllComments()
    return render_template('index.html', title='Home', users=users, topics=topics, comments=comments)
    
@app.route('/create_topic', methods = ['GET', 'POST'])
def createTopic():
    form = TopicForm()
    if form.validate_on_submit():
        DatabaseManager.addTopic(user_id=current_user.id,title=form.title.data,body=form.body.data)
        return redirect(url_for('home'))
    return render_template('create_topic.html', title='Create New Topic', form=form)
