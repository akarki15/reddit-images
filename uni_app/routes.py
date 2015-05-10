import os
from uni_app import app
from flask import Flask, render_template, request, url_for, flash, session, redirect, send_from_directory
from forms import SignInForm, SignUpForm, CreatePostForm, CreateCommunityForm
from models import db, User, Post, Category
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
			# also store the userID
			user = User.query.filter_by(username = form.username.data.lower()).first()
			session['userID'] = user.userID			
      		return redirect(url_for('profile'))
	elif request.method == 'GET':
		return render_template('signin.html', form=form,communityform=CreateCommunityForm())

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
		user = User.query.filter_by(username = form.username.data.lower()).first()
		session['userID'] = user.userID			
		return redirect(url_for('profile'))
		
   
  elif request.method == 'GET':
	return render_template('signup.html', form=form,communityform=CreateCommunityForm())

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
				return render_template('profile.html', form=form,communityform=CreateCommunityForm())
			else:				
				newpost = Post(form.text.data, session['userID'], form.categoryID)				
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
										
					
				db.session.commit()
				
				flash("posted!")			
				return redirect(url_for('profile'))
		elif request.method == 'GET':		
			# posts = Post.query.filter_by(username = session['username']).first()
			return render_template('profile.html', form=form, communityform=CreateCommunityForm())

@app.route('/community', methods=['GET', 'POST'])
def community():	
	communityform= CreateCommunityForm()
	user = User.query.filter_by(username = session['username']).first()
	if user is None:
		return redirect(url_for('signin'))
	else:
		if request.method == 'POST':
			newCategory = Category(communityform.category.data.lower())					
			db.session.add(newCategory)
			db.session.commit()			
			communityform.message= "Community created!"			
		# returns all the community list
		# elif request.method == 'GET':
		return render_template('profile.html', form=CreatePostForm(), communityform=communityform)

@app.route('/signout')
def signout():
 
	if 'username' not in session:
		return redirect(url_for('signin'))
	# remove the cookie stored in the user account
	session.pop('username', None)
	session.pop('userID', None)
	flash("Signed out!")
	return redirect(url_for('signin'))

@app.route('/frontpage')
def frontpage():
 
	if 'username' not in session:
		return redirect(url_for('signin'))
	posts = Post.query.all();
	for post in posts:
		post.username = User.query.filter_by(userID = post.userID).first().username				
		post.communityName = Category.query.filter_by(categoryID = post.categoryID).first().name				
		if post.imageURI != None:
			post.fullImageURI = url_for('static',filename=("img/"+str(post.imageURI)))		
	return render_template('frontpage.html', posts=posts, communityform=CreateCommunityForm())


if __name__ == '__main__':
  app.run(debug=True)