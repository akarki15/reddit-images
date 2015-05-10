from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
  
db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  userID = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  username = db.Column(db.String(120), unique=True)
  hashpass = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, username, password):
	self.firstname = firstname.title()
	self.lastname = lastname.title()
	self.username = username.lower()
	self.set_password(password)
	 
  def set_password(self, password):
	self.hashpass = generate_password_hash(password)
   
  def check_password(self, password):
	return check_password_hash(self.hashpass, password)

class Post(db.Model):
	__tablename__ = 'posts'
	postID = db.Column(db.Integer, primary_key = True)
	text = db.Column(db.String(1000))
	imageURI= db.Column(db.String(100))
	userID = db.Column(db.Integer, db.ForeignKey('users.userID'))
	categoryID = db.Column(db.Integer, db.ForeignKey('categories.categoryID'))
	
	def __init__(self, text, userID, categoryID):
		self.text = text.title()				
		# self.imageURI = imageURI.title()
		self.userID = userID
		self.categoryID= categoryID


class Category(db.Model):
	__tablename__ = 'categories'
	categoryID = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(1000))
	
	def __init__(self, name):
		self.name = name				
		

