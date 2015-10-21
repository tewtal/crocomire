from flask.ext.wtf import Form
from wtforms import SelectField, SelectMultipleField, TextAreaField, StringField, validators, ValidationError

class AddForm(Form):
	game = SelectField(u'Game', [validators.Required()], choices=(), coerce=int)
	area = SelectField(u'Area', [validators.Required()], choices=(), coerce=int)
	room = SelectField(u'Room', [validators.Required()], choices=(), coerce=int)
	categories = SelectField(u'Category', [validators.Required()], choices=(), coerce=int)
	name = StringField(u'Name', [validators.Required()])
	description = TextAreaField(u'Description', [validators.Required()], description=u'HTML input is allowed (be careful).')
	difficulty = SelectField(u'Difficulty', choices=[(1,'Beginner'),(2,'Intermediate'),(3,'Advanced')], coerce=int)
	video = StringField(u'Video', [validators.Optional(), validators.URL()])
	new_roomname = StringField(u'New room name')
	new_roomlink = StringField(u'New room link', [validators.Optional(), validators.URL()])

	def validate_new_roomname(form, field):
		if form.room.data == -1:
			if len(field.data) == 0:
				raise ValidationError('This field is required.')
	
