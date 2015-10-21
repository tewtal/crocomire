from datetime import datetime
from crocomire import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
	__tablename__ = "users"
	id = db.Column('user_id', db.Integer, primary_key = True)
	username = db.Column('username', db.String(255), unique=True, index=True)
	password = db.Column('password', db.String(255))
	email = db.Column('email', db.String(255), unique=True, index=True)
	flags = db.Column('flags', db.String(50))
	registered_on = db.Column('registered_on', db.DateTime)
	strats = db.relationship('Strat', backref='user', lazy='dynamic')

	def __init__(self, username, password, email):
		self.username = username
		self.set_password(password)
		self.email = email
		self.flags = ""
		self.registered_on = datetime.utcnow()
	
	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True
	
	def is_anonymous(self):
		return False
	
	def get_id(self):
		return unicode(self.id)
	
	def __repr__(self):
		return '<User %r>' % (self.username)

class Game(db.Model):
	__tablename__ = "games"
	id = db.Column('game_id', db.Integer, primary_key = True)
	name = db.Column('name', db.String(255))
	description = db.Column('description', db.Text())
	short_name = db.Column('short_name', db.String(255))
	link = db.Column('link', db.Text())
	areas = db.relationship('Area', backref='game', lazy='dynamic')
	strats = db.relationship('Strat', backref='game', lazy='dynamic')

	def __init__(self, name, description = "", link = ""):
		self.name = name
		self.description = description
		self.link = link


class Area(db.Model):
	__tablename__ = "areas"
	id = db.Column('area_id', db.Integer, primary_key = True)
	name = db.Column('name', db.String(255))
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
	strats = db.relationship('Strat', backref='area', lazy='dynamic')
	rooms = db.relationship('Room', backref='area', lazy='dynamic')

	def __init__(self, name, game_id):
		self.name = name
		self.game_id = game_id

class Room(db.Model):
	__tablename__ = "rooms"
	id = db.Column('room_id', db.Integer, primary_key = True)
	name = db.Column('name', db.String(255))
	link = db.Column('link', db.Text())
	area_id = db.Column(db.Integer, db.ForeignKey('areas.area_id'))
	strats = db.relationship('Strat', backref='room', lazy='dynamic')

	def __init__(self, name, link, area_id):
		self.name = name
		self.link = link
		self.area_id = area_id


class Category(db.Model):
	__tablename__ = "categories"
	id = db.Column('category_id', db.Integer, primary_key = True)
	name = db.Column('name', db.String(255))
	glitched = db.Column(db.Integer)
	strats = db.relationship('Strat', backref='category', lazy='dynamic')


class Strat(db.Model):
	__tablename__ = "strats"
	id = db.Column('strat_id', db.Integer, primary_key = True)
	name = db.Column('name', db.String(255))
	description = db.Column('description', db.Text())
	link = db.Column('link', db.Text())
	difficulty = db.Column(db.Integer)
	created_on = db.Column('created_on', db.DateTime)
	
	area_id = db.Column(db.Integer, db.ForeignKey('areas.area_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
	room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
	game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))

	def __init__(self, name, description, link, difficulty, user_id, area_id, room_id, category_id, game_id):
		self.name = name
		self.description = description
		self.link = link
		self.difficulty = difficulty
		self.user_id = user_id
		self.area_id = area_id
		self.room_id = room_id
		self.game_id = game_id
		self.category_id = category_id
		self.created_on = datetime.utcnow()
	
	def get_difficulty_color(self):
		if self.difficulty == 1:
			return "success"
		elif self.difficulty == 2:
			return "warning"
		elif self.difficulty == 3:
			return "danger"
	
	def get_difficulty_name(self):
		if self.difficulty == 1:
			return "Beginner"
		elif self.difficulty == 2:
			return "Intermediate"
		elif self.difficulty == 3:
			return "Advanced"

	def get_embed(self):
		if 'youtube' in self.link:
			return self.link.replace("watch?v=", "embed/")
		elif 'twitch' in self.link:
			parm_pos = self.link.rfind("?")
			if parm_pos == -1:
				parm_pos = len(self.link)

			vid_pos = self.link.rfind("/", 0, parm_pos)
			chan_pos = self.link.rfind("/", 0, vid_pos - 3)

			channel = self.link[chan_pos+1:vid_pos-2]
			vid = self.link[vid_pos-1:vid_pos] + self.link[vid_pos+1:parm_pos]
			parm = ""
			if parm_pos != len(self.link):
				parm = self.link[parm_pos:].replace("?","&").replace("t=","initial_time=")
				it = parm.rfind("=")
				tm = parm[it+1:]
				mm = int(tm[:tm.find("m")])
				ss = int(tm[tm.find("m")+1:tm.find("s")])
				parm = parm[:it+1] + str(mm*60 + ss)


			#return "http://player.twitch.tv/?volume=1&video=%s" % (vid)
			return "channel=%s&volume=100&videoId=%s&auto_play=true%s" % (channel, vid, parm)
		else:
			return self.link

