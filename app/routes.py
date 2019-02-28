from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, SubmitForm, DeleteForm
from app.models import User, Post
from datetime import datetime

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.filter(Post.deleted == False).order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html',
	 title = 'Front page', posts=posts.items, next_url=next_url, prev_url=prev_url)

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

@login_required
@app.route('/delete/<post_id>')
def delete(post_id):
	post = Post.query.filter_by(id=post_id).first()
	if post:
		if not post.deleted:
			post.deleted = True
			post.deleted_timestamp = datetime.utcnow()
			db.session.commit()
			flash('Link deleted.')
			return redirect(url_for('index'))
		else:
			flash('Link is already deleted')
			return redirect(url_for('index'))
	flash("Link doesn't exist.")
	return redirect(url_for('index'))

@app.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user:
		posts = Post.query.filter_by(user_id=user.id).all()
		if posts:
			return render_template('user.html', user=user, posts=posts)
		return render_template('user.html', user=user)
	return redirect(url_for('index'))
    