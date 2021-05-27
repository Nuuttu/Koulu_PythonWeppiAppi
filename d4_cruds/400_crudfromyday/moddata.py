from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app=Flask(__name__)
app.secret_key="UfSLFCoRRPcLv07PW0lethoLHUD"
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
    db.session.add(Todo(task="bfr_request", time="0"))
    db.session.add(Todo(task="bfr_r2", time="2"))
    db.session.commit()

@app.route('/add', methods=["GET", "POST"])
def addForm():
    form = TodoForm()
    if form.validate_on_submit():
  	    todo = Todo()
  	    form.populate_obj(todo)
  	    db.session.add(todo)
  	    db.session.commit()
  	    flashmessage = "Task added: " + todo.task
  	    flash(flashmessage, "Add")
  	    return redirect("/")
    return render_template("add.html", form=form)

@app.route('/delete/<int:todoID>', methods=['GET', 'DELETE'])
def deleteItem(todoID):
    dtodo = Todo.query.get(todoID)
    db.session.delete(dtodo)
    db.session.commit()
    flash("deleted: " + dtodo.task)
    return redirect('/')

@app.route('/edit/<int:todoID>', methods=['GET', 'POST'])
def editTodo(todoID):
    todo = Todo.query.get(todoID)
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        form.populate_obj(todo)       
        db.session.commit()
        flashmessage = "Task edited: " + todo.task
        flash(flashmessage, "Edit")
        return redirect("/")
    return render_template("edit.html", todo=todo, form=form)

@app.route('/')
def base():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

if __name__ == "__main__":
    app.run(debug=True)