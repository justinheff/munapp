
## TODO: Change this so ID's are added automatically

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import app
from app import db
from app.models import User, Topic, Comment, Group, group_identifier

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
def addTopic(user_id, title, body, group_id, public=True):
    ## Initialize topic attributes
    topic = Topic()
    topic.user_id = user_id
    topic.title = title
    topic.body = body
    topic.public = public
    topic.group_id = group_id
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

## Get specific comment from database
def getComment(id):
	comment = Comment.query.get(id)
	return comment

## Edit specific comment and commit to database
def editComment(id, body):
    comment = getComment(id)
    comment.body = body
    db.session.commit()
    
## Edit specific topic and commit to database
def editTopic(id, title, body):
    topic= getTopic(id)
    topic.title = title
    topic.body = body
    db.session.commit()
    
## Get specific group from database
def getGroup(id):
	group = Group.query.get(id)
	return group

## Add group to database
def addGroup(name):
    group = Group()
    group.name = name
    group.members.append(current_user)
    db.session.add(group)
    db.session.commit()

## Add member to specified group    
def addGroupMember(user,group):
    group.members.append(user)
    db.session.commit()
    
## Get specific user by user ID
def getUser(id):
    user = User.query.get(id)
    return user

## Get specific user by username from database    
def getUserByUsername(username):
    """Searches the database for a given username"""
    user = User.query.filter_by(username=username).first()
    return user

## Check if a user is a member of a group    
def checkMember(user,group):
    """Check if a user is a member of a group"""
    if user in group.members:
        return True
    else:
        return False
        
def getAllPublicTopics():
    """Returns all topics that have None as their group id (ie. all public topics)"""
    topics = Topic.query.filter_by(group_id=None)
    return topics

def checkTopicAuthor(user,topic):
    """Check if the current user is the author of a topic - used for when editing a topic"""
    if user.id is topic.author.id:
        return True
    else:
        return False
        
def checkCommentAuthor(user,comment):
    """Check if the user is the author of a comment - used for when editing a comment"""
    if user.id is comment.author.id:
        return True
    else:
        return False
    
