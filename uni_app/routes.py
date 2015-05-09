import os
from uni_app import app
from flask import Flask, render_template, request, url_for, flash, session, redirect
from forms import SignInForm, SignUpForm, CreatePostForm
from models import db, User, Post
from werkzeug import secure_filename
from settings import APP_UPLOADS


@app.route('/', methods=['GET','POST'])
def signin():	
	form = SignInForm()	
	

	if request.method == 'POST':		
		if form.validate() == False:			
			return render_template('signin.html', form=form)
		else:
			session['username'] = form.username.data
      		return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signin.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUpForm()
   
  if request.method == 'POST':
	if form.validate() == False:
		flash ("Wow, that didn't work!")
		return render_template('signup.html', form=form)
	else:   		
		newuser = User(form.firstname.data, form.lastname.data, form.username.data, form.password.data)
		db.session.add(newuser)
		db.session.commit()
		# hashes the username as an ecrypted ID and stores as a cookie in the user's browser
		session['username'] = newuser.username
		return redirect(url_for('profile'))
		return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
   
  elif request.method == 'GET':
	return render_template('signup.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile(): 

	form = CreatePostForm()
	# session gets the encrypted ID and hashes it to get the value i.e. the username
	user = User.query.filter_by(username = session['username']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':			
			if form.validate() == False:				
				return render_template('profile.html', form=form)
			else:				
				newpost = Post(form.text.data, 2, form.tags.data)				
				db.session.add(newpost)
				
				file = request.files[form.image.name]				
				if file: 					
					filename = secure_filename(file.filename)
					# flush to ge the postID to be used as filename
					db.session.flush()				
					filename = str(newpost.postID) + os.path.splitext(filename)[1]
					newpost.imageURI = filename
					file.save(os.path.join(APP_UPLOADS, filename))								
					flash(filename+" uploaded!")		
					
					print 'filename:', filename									
					
				db.session.commit()
				
				flash("posted!")			
				return redirect(url_for('profile'))
		elif request.method == 'GET':		
			# posts = Post.query.filter_by(username = session['username']).first()
			return render_template('profile.html', form=form)

	
	

@app.route('/signout')
def signout():
 
	if 'username' not in session:
		return redirect(url_for('signin'))
	# remove the cookie stored in the user account
	session.pop('username', None)
	flash("Signed out!")
	return redirect(url_for('signin'))

@app.route('/frontpage')
def frontpage():
 
	if 'username' not in session:
		return redirect(url_for('signin'))
	# remove the cookie stored in the user account
	session.pop('username', None)
	flash("Signed out!")
	return redirect(url_for('signin'))

if __name__ == '__main__':
  app.run(debug=True)