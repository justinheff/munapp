
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app import db
from app import DatabaseManager
from app.forms import RegistrationForm, LoginForm, TopicForm, CommentForm, GroupForm, AddUserForm
from app.models import User,Topic,Comment,Group
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
    topics = DatabaseManager.getAllPublicTopics()
    comments = DatabaseManager.getAllComments()
    return render_template('index.html', title='Home', users=users, topics=topics, comments=comments)
 
@app.route('/create_topic/', methods = ['GET', 'POST'])
@app.route('/create_topic/<group_id>', methods = ['GET', 'POST'])
@login_required
def createTopic(group_id=None):
    form = TopicForm()
    if form.validate_on_submit():
        DatabaseManager.addTopic(user_id=current_user.id,title=form.title.data,body=form.body.data,group_id=group_id)
        if group_id is None:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('viewGroup',id=group_id))
    return render_template('create_topic.html', title='Create New Topic', form=form)
	
@app.route('/post/<id>', methods = ['GET', 'POST'])
@login_required
def viewTopic(id):
    form = CommentForm()
    topic = DatabaseManager.getTopic(id)
    comments = DatabaseManager.getTopicComments(id)
    if topic.group_id is not None:
        group = DatabaseManager.getGroup(topic.group_id)
        if DatabaseManager.checkMember(current_user,group):
            if form.validate_on_submit():
                DatabaseManager.addComment(user_id=current_user.id,topic_id=id,body=form.comment.data)
                return redirect(url_for('viewTopic',id=id))
            return render_template('post.html', title='View Topic',topic=topic,comments=comments,form=form)
        else:
            flash('You are not a member of the group this topic belongs to')
            return redirect(url_for('home'))
    else:
        if form.validate_on_submit():
            DatabaseManager.addComment(user_id=current_user.id,topic_id=id,body=form.comment.data)
            return redirect(url_for('viewTopic',id=id))
        return render_template('post.html', title='View Topic',topic=topic,comments=comments,form=form)
    
@app.route('/edit_comment/<id>', methods = ['GET', 'POST'])
@login_required
def editComment(id):
    form = CommentForm()
    comment = DatabaseManager.getComment(id)
    if DatabaseManager.checkCommentAuthor(current_user,comment):
        if form.validate_on_submit():
            DatabaseManager.editComment(id=id,body=form.comment.data)
            return redirect(url_for('viewTopic',id=comment.topic_id))
        return render_template('edit_comment.html', title='Edit Comment',form=form,comment=comment)
    else:
        flash('You are not eligible to edit this comment')
        return redirect(url_for('home'))

@app.route('/edit_topic/<id>', methods = ['GET', 'POST'])
@login_required
def editTopic(id):
    form = TopicForm()
    topic = DatabaseManager.getTopic(id)
    if DatabaseManager.checkTopicAuthor(current_user,topic):
        if form.validate_on_submit():
            DatabaseManager.editTopic(id=id,title=form.title.data, body=form.body.data)
            return redirect(url_for('viewTopic',id=id))
        return render_template('edit_topic.html', title='Edit Topic',form=form,topic=topic)
    else:
        flash('You are not elgible to edit this topic')
        return redirect(url_for('home'))
        
@app.route('/create_group', methods = ['GET', 'POST'])
@login_required    
def createGroup():
    ## Allows current user to create a new group
    form = GroupForm()
    if form.validate_on_submit():
        DatabaseManager.addGroup(name=form.name.data)
        return redirect(url_for('home'))
    return render_template('create_group.html',form=form)
    
@app.route('/my_groups', methods = ['GET', 'POST'])
@login_required
def myGroups():
    ## TESTING ONLY - WILL BE REMOVED WHEN PROFILES ARE DONE
    ## Shows a user's current groups
    return render_template('my_groups.html', title='My Groups')
    
@app.route('/group/<id>', methods = ['GET', 'POST'])
@login_required
def viewGroup(id):
    group = DatabaseManager.getGroup(id)
    if DatabaseManager.checkMember(current_user,group):
        form = AddUserForm()
        if form.validate_on_submit():
            user = DatabaseManager.getUserByUsername(form.username.data)
            if user is None:
                flash('No such user exists')
            else:
                DatabaseManager.addGroupMember(user=user,group=group)
                return render_template('group.html', group=group, title=group.name,form=form)
        return render_template('group.html', group=group, title=group.name,form=form)
    else:
        flash('You are not a member of the specified group')
        return redirect(url_for('home'))
    