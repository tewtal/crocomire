from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)
app.debug = True
app.config.from_object('crocomire.settings')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

import crocomire.models
import crocomire.auth
import crocomire.views
from crocomire.models import User, Game


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	g.game = Game.query.get(1)
