from flask import *
from flask_mysqldb import MySQL 
from login import login as log 
from todo import addToDo
from wtforms import StringField, PasswordField, Form, validators
app=Flask(__name__)
app.config['SECRET_KEY']='customer@123'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='myflask'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
	form=log(request.form)
	if request.method=="POST" and form.validate():
		cur=mysql.connection.cursor()
		email=form.email.data
		password=form.password.data
		cur.execute("SELECT email,password FROM login_details WHERE email=%s AND password=%s",(email,password))
		validate=cur.fetchone()
		if len(validate)!=0:
			cur.execute("SELECT name FROM login_details WHERE email=%s AND password=%s",(email,password))
			data=cur.fetchone()
			session['is_login']=True
			session['priority']=False
			session['name']=data['name']
			return redirect(url_for('dashboard'))
	return render_template('login.html',form=form)
@app.route('/logout')
def logout():
	session['is_login']=False;
	session.clear()
	return redirect(url_for('login'))
@app.route('/dashboard')
def dashboard():
	cur=mysql.connection.cursor()
	name=session['name']
	cur.execute("SELECT todo FROM todos WHERE name=%s",(name,))
	data=cur.fetchall()
	return render_template('dashboard.html',validate=data)
@app.route('/add_todo',methods=['GET','POST'])
def add_todo():
	form=addToDo(request.form)
	if request.method=="POST" and form.validate():
		todo=form.todo.data
		priority=form.priority.data
		if session['priority']==False and priority==True:
			session['priority']=True
		else:
			if session['priority']==True and priority==True:
				priority=False
		name=session['name']
		cur=mysql.connection.cursor()
		cur.execute("INSERT INTO todos(todo,priority,name) VALUES(%s,%s,%s)",(todo,int(priority),name))
		mysql.connection.commit()
		cur.close()		
		return redirect(url_for('dashboard'));
	return render_template('addTodo.html',form=form)
if __name__=="__main__":
	app.run('localhost',4200,debug=True)