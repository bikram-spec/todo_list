from wtforms import StringField, PasswordField, BooleanField, Form, validators
class addToDo(Form):
	todo=StringField('ToDo Title',[validators.Length(min=10),validators.DataRequired()])
	priority=BooleanField('priority')