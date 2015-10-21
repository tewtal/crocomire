from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g, jsonify
from flask.ext.login import login_user , logout_user , current_user , login_required
from crocomire import app, db
from crocomire.models import Game, Area, Room, Category, Strat
from crocomire.forms import AddForm
from sqlalchemy import or_

@app.route('/')
@app.route('/<string:game_name>')
def index(game_name=None):
	if game_name:
		if game_name == "favicon.ico":
			abort(404)

		game = Game.query.filter(Game.short_name == game_name).first()
		if game:
			g.game = game
		else:
			flash('That game is not in the database')

	strats = Strat.query.order_by(Strat.area_id.desc()).order_by(Strat.name.desc()).filter(Strat.game_id == g.game.id)

	if(request.args.get('s')):
		search = ('%%%s%%' % request.args.get('s'))
		strats = strats.filter(or_(Strat.name.like(search), Strat.description.like(search)))
	
	if(request.args.get('a')):
		area = request.args.get('a')
		strats = strats.filter(Strat.area_id == area)
	
	if(request.args.get('r')):
		room = request.args.get('r')
		strats = strats.filter(Strat.room_id == room)
	
	if(request.args.get('c')):
		category = request.args.get('c')
		strats = strats.filter(Strat.category_id == category)

	return render_template('index.html',
		strats = strats.all(),
	)

@app.route('/<int:strat_id>')
def strat(strat_id):
	strat = Strat.query.get(strat_id)
	if not strat:
		flash("That strategy doesn't exist")
		return redirect(url_for('index'))
	
	return render_template('strat.html', strat = strat)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = AddForm(request.form)
	games = [(gg.id, gg.name) for gg in Game.query.all()]
	game = games[0][0] if not request.form else int(request.form['game'])
	
	areas = [(a.id, a.name) for a in Area.query.filter_by(game_id = game).all()]
	area = areas[0][0] if not request.form else int(request.form['area'])

	rooms = [(-1, 'Create new room...')] + [(r.id, r.name) for r in Room.query.filter_by(area_id = area).all()]
	categories = [(c.id, c.name) for c in Category.query.all()]
	
	form.game.choices = games
	form.area.choices = areas
	form.room.choices = rooms
	form.categories.choices = categories

	if request.method == 'POST' and form.validate():
		room_id = form.room.data
		if room_id == -1:
			new_room = Room(form.new_roomname.data, form.new_roomlink.data, form.area.data)
			db.session.add(new_room)
			db.session.commit()
			db.session.refresh(new_room)
			room_id = new_room.id

		strat = Strat(form.name.data, form.description.data, form.video.data, form.difficulty.data, g.user.id, form.area.data, room_id, form.categories.data, form.game.data)
		db.session.add(strat)
		db.session.commit()

		return redirect(url_for('index'))

	context = {
		'form': form,
	}

	return render_template('add.html', **context)

@app.route('/strats/edit/<int:strat_id>', methods=['GET', 'POST'])
@login_required
def edit(strat_id):
	strat = Strat.query.get(strat_id)
	
	if not strat:
		flash("That strategy doesn't exist")
		return redirect(url_for('index'))
	
	if strat.user_id != g.user.id and 'm' not in g.user.flags:
		flash("You don't have permission to edit that strategy")
		return redirect(url_for('index'))
	
	form = AddForm(request.form)

	games = [(gg.id, gg.name) for gg in Game.query.all()]
	game = strat.area.game_id if not request.form else int(request.form['game'])

	areas = [(a.id, a.name) for a in Area.query.filter_by(game_id = game).all()]
	area = strat.area_id if not request.form else int(request.form['area'])

	rooms = [(-1, 'Create new room...')] + [(r.id, r.name) for r in Room.query.filter_by(area_id = area).all()]
	room = strat.room_id if not request.form else int(request.form['room'])

	categories = [(c.id, c.name) for c in Category.query.all()]

	form.game.choices = games
	form.area.choices = areas
	form.room.choices = rooms
	form.categories.choices = categories

	if request.method == 'POST' and form.validate():
		room_id = form.room.data
		if room_id == -1:
			new_room = Room(form.new_roomname.data, form.new_roomlink.data, form.area.data)
			db.session.add(new_room)
			db.session.commit()
			db.session.refresh(new_room)
			room_id = new_room.id
	
		strat.name = form.name.data
		strat.description = form.description.data
		strat.link = form.video.data
		strat.difficulty = form.difficulty.data
		strat.area_id = form.area.data
		strat.room_id = room_id
		strat.category_id = form.categories.data
		strat.game_id = form.game.data
		db.session.commit()

		return redirect(url_for('index'))
	
	if not request.form:
		form.game.data = int(strat.game_id)
		form.area.data = int(strat.area_id)
		form.room.data = int(strat.room_id)
		form.name.data = strat.name
		form.description.data = strat.description
		form.categories.data = int(strat.category_id)
		form.video.data = strat.link
		form.difficulty.data = int(strat.difficulty)

	context = {
		'form': form,
	}
	
	return render_template('edit.html', **context)


@app.route('/strats/delete/<int:strat_id>', methods=['GET'])
@login_required
def delete(strat_id):
	strat = Strat.query.get(strat_id)
	
	if not strat:
		flash("That strategy doesn't exist")
		return redirect(url_for('index'))
	
	if strat.user_id != g.user.id and 'm' not in g.user.flags:
		flash("You don't have permission to delete that strategy")
		return redirect(url_for('index'))
	
	db.session.delete(strat)
	db.session.commit()

	return redirect(url_for('index'))

@app.route('/api/areas/<int:game_id>', methods=['GET'])
def areas(game_id):
	areas = Area.query.filter_by(game_id = game_id).all()
	return jsonify({'values': [(a.id, a.name) for a in areas]})

@app.route('/api/rooms/<int:area_id>', methods=['GET'])
def rooms(area_id):
	rooms = Room.query.filter_by(area_id = area_id).all()
	return jsonify({'values': [(-1, 'Create new room...')] + [(r.id, r.name) for r in rooms]})

@app.route('/api/strats/', methods=['GET'])
@app.route('/api/strats/<int:strat_id>', methods=['GET'])
@app.route('/api/strats/<string:strat_name>', methods=['GET'])
def strats(strat_id = None, strat_name = None):
	strats = []	
	if strat_id:
		strats = Strat.query.filter(Strat.id == strat_id).all()	
	elif strat_name:
		search = "%%%s%%" % (strat_name)
		strats = Strat.query.filter(or_(Strat.name.like(search), Strat.description.like(search))).all()
	else:
		strats = Strat.query.all()

	strat_dicts = []
	for s in strats:
		sd = {}
		sd['created_on'] = s.created_on
		sd['description'] = s.description
		sd['difficulty'] = s.difficulty
		sd['id'] = s.id
		sd['name'] = s.name
		sd['link'] = s.link
		sd['area_name'] = str(s.area.name)
		sd['room_name'] = s.room.name
		sd['category_name'] = s.category.name
		sd['game_name'] = s.game.name
		sd['user_name'] = s.user.username
		strat_dicts.append(sd)
	
	return jsonify({"strats": strat_dicts})

