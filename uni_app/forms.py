from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField, SubmitField,PasswordField
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Required
from models import db, User, Category

 
class SignInForm(Form):
	username = TextField("User", validators = [Required("Enter something for username!")])
	password = TextField("Password", validators = [Required("Enter something for lastname!")])
	submit = SubmitField("Send")

	# constructor 
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		print "IS THIS NOT WORKING!!!"
		if not Form.validate(self):
		  return False
		 
		user = User.query.filter_by(username = self.username.data.lower()).first()
		if user and user.check_password(self.password.data):
		  return True
		else:
		  self.username.errors.append ("Invalid username or password")
		  return False

class SignUpForm(Form):
	firstname = TextField("First name",  validators = [Required("Enter something for firstname!")])
	lastname = TextField("Last name",  validators = [Required("Enter something for lastname!")])
	username = TextField("User",  validators=[Required("Enter something for username!")])
	password = PasswordField('Password', validators =[Required("Enter something for password!")])
	submit = SubmitField("Create account")

	# Constructor calls the Form's default constructor
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	# Validate that the username does not exists 
	def validate(self):
		# check the form's default validator 
		if not Form.validate(self):
		  return False
		 
		user = User.query.filter_by(username = self.username.data.lower()).first()		
		if user:  
			self.username.errors.append(str(user.username) + "Username already taken")
		  	return False
		else:
			return True

class CreatePostForm(Form):
	text = TextField("Content",validators=[Required("Write something about this post!")])
	category = TextField("Category")
	image = FileField('Image File', validators = [FileAllowed(['jpg', 'png'], 'Images only!')])		
	submit = SubmitField("Post!")
	categoryID = ""

	# Constructor calls the Form's default constructor
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
	
	def validate(self):
		# check the form's default validator 
		if not Form.validate(self):
		  	return False
		category = Category.query.filter_by(name = self.category.data.lower()).first()				
		if not category:  
			self.category.errors.append(str(self.category.data) + " Community does not exist! Type an existing community's name or create one before posting!")
		  	return False
		else:			
			self.categoryID = category.categoryID			
			return True
class CreateCommunityForm(Form):			
	category = TextField("Name",validators=[Required("Community should have a name!")])	
	submit = SubmitField("Create!")	
	message = None	
	# Constructor calls the Form's default constructor
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
	
	def validate(self):
		# check the form's default validator 
		if not Form.validate(self):
		  	return False
		queryCategory = Category.query.filter_by(name = self.category.data.lower()).first()				
		if queryCategory:  
			self.category.errors.append(str(self.category.data) + " already exists!")
		  	return False
		else:						
			return True

	def getAllCommunities(self):
		for c in Category.query.all():
			print c.name
		return Category.query.all()