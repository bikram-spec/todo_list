from wtforms import StringField, PasswordField, Form, validators
class login(Form):
	email=StringField('Email',[validators.Length(min=5,max=50),validators.DataRequired()])
	password=PasswordField('Password',[validators.Length(min=5,max=15),validators.DataRequired()])