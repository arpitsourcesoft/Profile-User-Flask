# from os import environ
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)

# SECRET_KEY = environ.get('SECRET_KEY')
# adding configuration for using a sqlite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://arpit:Mysql-123@localhost/flask_db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Models
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), unique=False, nullable=False)
	last_name = db.Column(db.String(20), unique=False, nullable=False)
	age = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Name : {self.first_name}, Age: {self.age}"

# function to render index page
@app.route('/')
def index():
	profiles = Profile.query.all()
	return render_template('index.html', profiles=profiles)

@app.route('/add_data')
def add_data():
	return render_template('add_profile.html')

# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")
	age = request.form.get("age")

	if first_name != '' and last_name != '' and age is not None:
		p = Profile(first_name=first_name, last_name=last_name, age=age)
		db.session.add(p)
		db.session.commit()
		return redirect('/')
	else:
		return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
	data = Profile.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect('/')

# @app.route('/update/<int:id>')
# def update(id):
# 	data = Profile.query.get(id)
# 	db.session.update(data)
# 	db.session.commit()
# 	return redirect('/')

# @app.route('/api/v1/todo/<id>', methods=['PUT'])
# def update(id):
#    data = request.get_json()
#    get_todo = Todo.query.get(id)
#    if data.get('title'):
#        get_todo.title = data['title']
#    if data.get('todo_description'):
#        get_todo.todo_description = data['todo_description']
#    db.session.add(get_todo)
#    db.session.commit()
#    todo_schema = TodoSchema(only=['id', 'title', 'todo_description'])
#    todo = todo_schema.dump(get_todo)

#    return make_response(jsonify({"todo": todo}))

if __name__ == '__main__':
	app.run(debug=True, host='192.168.20.31', port='8080')
