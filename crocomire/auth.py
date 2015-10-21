import datetime
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask.ext.login import login_user , logout_user , current_user , login_required
from crocomire import app, db
from crocomire.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')

	if 'samus' not in request.form['question'].lower():
		flash('Incorrect answer to the security question')
		return redirect(url_for('register'))

	user = User.query.filter_by(username=request.form['username']).first()
	if user:
		flash('Username is already registered')
		return redirect(url_for('register'))

	try:
		user = User(request.form['username'], request.form['password'], request.form['email'])
		db.session.add(user)
		db.session.commit()
	except:
		flash('An error occured when registering the user')
		return redirect(url_for('register'))

	flash('User successfully registered')
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	
	username = request.form['username']
	password = request.form['password']
	remember_me = False

	if 'remember_me' in request.form:
		remember_me = True
	
	registered_user = User.query.filter_by(username=username).first()
	if registered_user is None:
		flash('Username is invalid', 'error')
		return redirect(url_for('login'))
	
	if not registered_user.check_password(password):
		flash('Password is invalid', 'error')
		return redirect(url_for('login'))
	
	login_user(registered_user, remember = remember_me)
	flash('Logged in successfully')
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
