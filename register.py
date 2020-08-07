from wtforms import Form, StringField, PasswordField, BooleanField, validators
from wtforms.fields.html5 import EmailField
class signup(Form):
	name=StringField('Name',[validators.Length(min=5,max=50),validators.DataRequired()])
	email=StringField('Email',[validators.Length(min=1,max=30),validators.DataRequired()])
	password=PasswordField('Password',[validators.DataRequired(),validators.Length(min=5,max=15),validators.EqualTo('confirm',message="Password Does not match")])
	confirm=PasswordField('confirm Password')