
## TODO: Change this so ID's are added automatically

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from app import app
from app import db
from app.models import User, Topic, Comment

## DEBUG: here to test and creating examples
## Get all users from the database
def getAllUsers():
    users = User.query.all()
    return users

def getAllPosts():
    posts = Post.query.all()
    return posts

## Get all comments in table
def getAllComments():
    comments = Comment.query.all()
    return comments

## Add user to database
def addUser(name, email, password):
    ## Create new user object, The form information has already been
    ## checked and validated by FlaskForm so there is no need to check again
    user = User(username=name, email=email)
    user.set_password(password)
    ## Add new user to the database and commit changes
    db.session.add(user)
    db.session.commit()
    ## DEBUG: This just displays a message so we know something happened
    ## TODO: Redirect the user to the main page here so they do not need to enter
    ##          their information into the login form
    flash('Congratulations, you are now a registered user!')

## Login user , users who are logged in are able to see and do more
def login(name, pw, remember_me):
    ## Get users and sort by username
    user = User.query.filter_by(username=name).first()
    ## Check if username is in database or if passwords match one in database
    if user is None or not user.check_password(pw):
        ## inform user of incorrect login information
        flash('Invalid username or password')
        ## Redirect user to the login page with error message displayed
        return redirect(url_for('login'))
    ## User information is correct, user flask_login to login user
    login_user(user, remember=remember_me)
    ## Set next page using request.args. If next is None then we send user to
    ## index page, if next has relevant URL we send user to that (found in 'next')
    ## This also keeps the site more secure and checks to see if the URL is relevant
    ## to our project (hackers could insert URL to a malicious site)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)

## User flask_login to log user out
def logout():
    logout_user()
    return redirect(url_for('home'))

## Add topic to database
def addTopic(user_id, title, body, public=True):
    ## Initialize topic attributes
    topic = Topic()
    topic.user_id = user_id
    topic.title = title
    topic.body = body
    topic.public = public
    ## add new topic to the database and commit the change
    db.session.add(topic)
    db.session.commit()
    ## DEBUG: Find a better way to confirm topic being successfully created to user
    ## Display a message to make sure this works
    flash('Topic created!')
	
def addComment(user_id, topic_id, body):
    ## Initialize comment attributes
    comment = Comment()
    comment.user_id = user_id
    comment.topic_id = topic_id
    comment.body = body
    ## add new comment to the database and commit the change
    db.session.add(comment)
    db.session.commit()
    ## DEBUG
    ## Display a message to make sure this works
    flash('Comment created!')

## Get all posts from the database
def getAllTopics():
    topics = Topic.query.all()
    return topics

## DEBUG:
## Get all comments on with topic_id = tid
def getTopicComments(tid):
    comments = Comment.query.filter_by(topic_id=tid)
    return comments

## Get specific topic from database
def getTopic(id):
	topic = Topic.query.get(id)
	return topic