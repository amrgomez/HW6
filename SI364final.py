# Import statements
import os
import requests
import json
from practice_api import api_key
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364projectplan_amrgomez" #change this later
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['HEROKU_ON'] = os.environ.get('HEROKU')

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

### ASSOCIATION TABLES ###
tags= db.Table('tags', db.Column('headlines_id',db.Integer,db.ForeignKey('headlines.id')),db.Column('articles_id',db.Integer, db.ForeignKey('articles.id')))
user_collection= db.Table('user_collection',db.Column('headlines_id',db.Integer,db.ForeignKey('headlines.id')), db.Column('articles_id', db.Integer, db.ForeignKey('articles.id')))

### TABLES ###
#Users and login
class User(db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    #relationship with articles saved
    collections= db.relationship('Articles', backref= 'User')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

#run flask_login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#retrieve news sources
class News(db.Model):
	__tablename__='news'
	id=db.Column(db.Integer,)
    term= db.Column(db.String(128))
    url= db.Column(db.String(256)) #newsource url
    def __repr__(self):
        "Headline:{0}, URL:{1}".format(self.term,self.url)

#retrieve articles
class Articles(db.Model):
	__tablename__='articles'
    id= db.Column(db.Integer,primary_key=True)
    article= db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    collection= db.relationship('Headlines', secondary= user_collection, backref= db.backref('Articles', lazy='dynamic'),lazy='dynamic')

#retrieve articles' headlines and urls
class Headlines(db.Model):
	__tablename__='headlines'
	id= db.Column(db.Integer, primary_key= True)
    term= db.Column(db.String(32), unique= True)
    # This model should have a many to many relationship with gifs (a search will generate many gifs to save, and one gif could potentially appear in many searches)
    headline= db.relationship('News', secondary=tags, backref=db.backref('Headlines',lazy='dynamic'),lazy='dynamic')
    # TODO 364: Define a __repr__ method for this model class that returns the term string
    def __repr__(self):
        return "Headlines: {0} (ID:{1})".format(self.id,self.term)

### LOGIN FORMS ###
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

### REQUEST FORMS ###
#Search headlines using term submitted
class HeadlineSearch(FlaskForm):
	search= StringField('Enter a term', validators= [Required()])
	submit= SubmitField('Submit')

class NewsSearch(FlaskForm):
	source= StringField('Enter a news source', validators= [Required()])
	submit= SubmitField('Submit')

### HELPER FUNCTIONS ###
#find news source from search term
def get_news_sources(search_string):
	pass
#find source's website
def get_source(id):
	pass
#finds source's picture (using html template)
def get_source_pic(title,url):
	pass
#create search term input
def get_or_create_search_term(term):
	pass

#### ERROR HANDLING ###
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

### ROUTES ###
@app.route('/', methods= ['GET','POST'])
def index():
	pass
@app.route('/search')
def terms():
	pass
@app.route('/headlines/<search_term>')
def headlines():
	pass

@app.route('/newsource')
def source():
	pass

@app.route('/gallery')
def pictures():
	pass

@app.route('all_searches',methods=['GET','POST'])
def collections():
	pass

#run app
if __name__ == '__main__':
    db.create_all()
    manager.run()




















