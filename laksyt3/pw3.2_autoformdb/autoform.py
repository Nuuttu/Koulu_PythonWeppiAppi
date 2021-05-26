from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app=Flask(__name__)
app.secret_key="VifF2g7V2qS61s638yaHk0FrWGQUP7"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)

TodoForm = model_form(Todo,
    base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def bfr():
    db.create_all()

    db.session.add(Todo(task="Run", time="30"))
    db.session.add(Todo(task="Fight", time="20"))
    db.session.add(Todo(task="Dance", time="50"))
    
    db.session.commit()
    

@app.route('/add', methods=["GET", "POST"])
def addForm():
    form = TodoForm()
    return render_template("add.html", form=form)

@app.route('/')
def base():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

if __name__ == "__main__":
    app.run(debug=True)