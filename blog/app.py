from flask import Flask , redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db' # models
db = SQLAlchemy(app)  # models


@app.route("/")
@app.route("/hello") # a function can have more routes
def say_hello():
    return "<p>Hello World!</p>"


@app.route("/home") 
def home():
    return render_template('_base.html',name='armin')


#   =======   Run Server   =======
# python -m flask --app A.app run

# ======================================================================================
from flask import render_template

@app.route("/name")
def user_name():
    return render_template('user_name.html',name='armin')


#  ======================================== models and sql ==============================

# pip install flask-sqlalchemy

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return f"Todo({self.id} - {self.content[:50]} - {self.date})"

###  in Terminal - to create db (like migrate)
# from app import app, db
# with app.app_context():
# [TAB] db.create_all()

### for create some data in db .just use this code one time . because return unique error 
# with app.app_context():
#     todo1 = Todo(content='hello to you 1')
#     todo1 = Todo(content='hello to you 2')
#     todo1 = Todo(content='hello to you 3')
#     db.session.add(todo1)
#     db.session.commit()

    
@app.route("/todo-list")
def todo_list():
    todo_list = Todo.query.all()
    # todo_list = Todo.query.filter_by(id=2)

    return render_template("todo_list.html", todo_list=todo_list)

@app.route("/todo-detail/<id>")
def todo_detail(id):
    todo = Todo.query.get(id) # get instance by primary key
    return render_template("todo_detail.html", todo=todo)

@app.route("/todo-delete/<id>")
def todo_delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_list'))




#  =====================================================================================

# to set changes without need to restart server
# in this code run server by : python app.py ("A" directory)
if __name__ == "__main__":
    app.run(debug=True)




