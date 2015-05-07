from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField, SubmitField,PasswordField, FileField
from wtforms.validators import Required
from models import db, User

 
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
			self.username.errors.append("Username already taken")
		  	return False
		else:
			return True

class CreatePostForm(Form):
	text = TextField("Content",validators=[Required("Write something about this post!")])
	tags = TextField("Tags")
	image        = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])	
	submit = SubmitField("Post!")

	# Constructor calls the Form's default constructor
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
	
	def validate(self):
		# check the form's default validator 
		if not Form.validate(self):
		  	return False
		else:
			return True
