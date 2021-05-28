from flask import Flask, render_template, redirect, flash, session, abort
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators

app = Flask(__name__)
app.secret_key="cvhQr6otEjf8O8YdSO6U7liDu6ycoz"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)

TodoForm = model_form(Todo, base_class=FlaskForm, db_session=db.session)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
    email = StringField("email", validators=[validators.Email()])
    password = PasswordField("password", validators=[validators.InputRequired()])


## CurrentUser config

def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None
    return User.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser

## user view

@app.route("/register", methods=["GET", "POST"])
def registerUser():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash("User already exist. Log in")
            return redirect("/login")
        
        user = User(email=email)
        user.setPassword(password)

        db.session.add(user)
        db.session.commit()
        
        flash("added a account. now login")
        return redirect("/login")
        
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def loginUser():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Login failed.")
            return redirect("/login")
        if not user.checkPassword(password):
            flash("Login failed.")
            return redirect("/login")
        
        session["uid"]=user.id
        flash("Login success")
        return redirect("/")
        
    return render_template("login.html", form=form)


@app.route("/logout")
def logoutUser():
    session["uid"] = None
    flash("Logged out.")
    return redirect("/")

## Main view

@app.before_first_request
def initDb():
    db.create_all()
    db.session.add(Todo(task="Run"))
    db.session.add(Todo(task="All I Need"))
    user = User(email="asd@asd.asd")
    user.setPassword("asd")
    db.session.add(user)
    
    db.session.commit()

@app.route("/")
def base():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")

@app.errorhandler(403)
def custom403(e):
    flash("You need to log in to do this.")
    return redirect("/")


@app.route("/todo/<int:id>/edit", methods=["GET", "POST"])
@app.route("/todo/add", methods=["GET", "POST"])
def addTodo(id=None):
    if not currentUser():
            abort(403)
    todo = Todo()
    message = "Add Todo"
    flashmessage = "Added Todo: "
    pageTitle = "Add - Adds and Todos"
    if id:
        todo = Todo.query.get_or_404(id)
        message = "Edit Todo: " + todo.task
        flashmessage = "Edited " + todo.task  +" -> "
        pageTitle = "Edit - Todos and Tasks"
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
    if not currentUser():
        abort(403)
    todo = Todo.query.get_or_404(id)
    return render_template("delete.html", todo=todo)   

@app.route("/<int:id>/annihilate")
def annihilateTodo(id):
    if not currentUser():
        abort(403)
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash("Deleted todo: - " + todo.task)
    return redirect("/")
    
    
if __name__ == "__main__":
    app.run(debug=True)