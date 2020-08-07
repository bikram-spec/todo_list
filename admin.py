from flask import *
from register import signup
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, BooleanField, validators
app=Flask(__name__)
app.config['SECRET_KEY'] = 'vikram123'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='myflask'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql=MySQL(app)
@app.route('/admin')
@app.route('/')
def index():
	cur=mysql.connection.cursor()
	cur.execute("SELECT name,email,password FROM login_details")
	rc=cur.fetchall()
	#rc=str(rc)
	return render_template('admin.html',record=rc)

@app.route('/register',methods=['GET','POST'])
def register():
	form=signup(request.form)
	if request.method=="POST" and form.validate():
		name=form.name.data
		email=form.email.data
		password=form.password.data

		cur=mysql.connection.cursor()
		cur.execute("INSERT INTO login_details(name,email,password) VALUES(%s, %s, %s)",(name,email,password))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('index'))
	return render_template('register.html',form=form)
@app.route('/dashboard/<name>')
def classfier(name):
	cur=mysql.connection.cursor()
	cur.execute("SELECT todo FROM todos WHERE name=%s",(name,))
	data=cur.fetchall()
	return render_template('classfier.html',records=data)
@app.route('/Priority')
def priority():
	cur=mysql.connection.cursor()
	cur.execute("SELECT todo FROM todos WHERE priority=1")
	data=cur.fetchall()
	cur.close()
	return render_template('priority.html',data=data)
if __name__=="__main__":
	app.run(debug=True)