from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key="cvhQr6otEjf8O8YdSO6U7liDu6ycoz"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)

TodoForm = model_form(Todo, base_class=FlaskForm, db_session=db.session)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

UserForm = model_form(User, base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initDb():
    db.create_all()
    db.session.add(Todo(task="Run"))
    db.session.commit()

@app.route("/")
def base():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")

@app.route("/todo/<int:id>/edit", methods=["GET", "POST"])
@app.route("/todo/add", methods=["GET", "POST"])
def addTodo(id=None):
    todo = Todo()
    message = "Add Todo"
    flashmessage = "Added Todo: "
    pageTitle = "Add Todo"
    if id:
        todo = Todo.query.get_or_404(id)
        message = "Edit Todo: " + todo.task
        flashmessage = "Edited " + todo.task  +" -> "
        pageTitle = "Edit Todo"
    form = TodoForm(obj=todo)
    if form.validate_on_submit():
        form.populate_obj(todo)
        db.session.add(todo)
        db.session.commit()
        flash(flashmessage + todo.task)
        return redirect("/")
    return render_template("add.html", form=form, pageTitle=pageTitle)

@app.route("/todo/<int:id>/delete")
def deleteTodo(id):
    todo = Todo.query.get_or_404(id)
    return render_template("delete.html", todo=todo)

@app.route("/<int:id>/annihilate")
def annihilateTodo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def registerUser():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        if check_password_hash(user.password, form.password.data):
            pswd = form.password.data
        else:
            pswd = "NOOOoo"
        flash("Registered new user: > " + user.email + " < and hashed password:  > " + pswd + " <")
        return redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def loginUser():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            loginMsg = "Logged in successfully"
        else:
            loginMsg = "NOOOoo"
        flash(loginMsg)
        return redirect("/")
    return render_template("login.html", form=form)
if __name__ == "__main__":
    app.run()