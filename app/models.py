from datetime import datetime
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	karma = db.Column(db.Integer)
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	

	def __repr__(self):
		return '<User {}>'.format(self.username)   

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	url = db.Column(db.String(512))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	score = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


	def __repr__(self):
		return '<Post {}>'.format(self.body)