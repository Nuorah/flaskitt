from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, SubmitForm
from app.models import User, Post

@app.route('/')
@app.route('/index')
#@login_required
def index():
	posts = Post.query.all()
	return render_template('index.html', title = 'Front page', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@login_required
@app.route('/submit', methods=['GET', 'POST'])
def submit():
	form = SubmitForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, url = form.url.data, user_id = current_user.id)
		db.session.add(post)
		db.session.commit()
		flash('Link submitted.')
		return redirect(url_for('index'))
	return render_template('submit.html', title='Submit', form=form)