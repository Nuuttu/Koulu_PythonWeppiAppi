from flask import Flask, render_template, flash, session, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators


app = Flask(__name__)
app.secret_key="l3OdE9Y5pLIU2RIulDi8pLv9xLmFQW"
db = SQLAlchemy(app)


## database handling

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, foreign_key=True)
    text = db.Column(db.String(160), nullable=False)

ChapterForm = model_form(Chapter, base_class=FlaskForm, db_session=db.session, exclude=["owner"])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

class UserForm(FlaskForm):
    username = StringField("username", validators=[validators.InputRequired()])
    password = PasswordField("password", validators=[validators.InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[validators.InputRequired()])
    password = PasswordField("password", validators=[validators.InputRequired()])
    registerKey = StringField("registerKey", validators=[validators.InputRequired()])


## User Handling

def currentUser():
    try:
        uid = int(session["uid"])
    except:
        return None
    return User.query.get(uid)

app.jinja_env.globals["currentUser"] = currentUser

def loggedIn():
    if not currentUser():
        return abort(403)

@app.route("/register", methods=["GET", "POST"])
def registerUser():
    form =form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        registerKey = form.registerKey.data

        if User.query.filter_by(username=username).first():
            flash("User already exist. Log in")
            return redirect("/login")
        if not registerKey == "cube":
            flash("Wrong register key. You need to know this in order to register.")
            return redirect("/register")
        user = User(username=username)
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
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Login failed.")
            return redirect("/login")
        if not user.checkPassword(password):
            flash("Login failed.")
            return redirect("/login")

        session["uid"]=user.id
        flash("Login success. Hello " + currentUser().username)
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logoutUser():
    session["uid"] = None
    flash("Logged out.")
    return redirect("/")


## main view

@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")

@app.errorhandler(403)
def custom403(e):
    flash("You don't have a permission to do that")
    return redirect("/")

@app.before_first_request
def initApp():
    db.create_all()

    user = User(username="asd")
    user.setPassword("asd")
    db.session.add(user)
    db.session.add(Chapter(text="Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum ", owner=1))
    db.session.add(Chapter(text="Lorem ipsum Lorem ipsum Lorem asdasd ddasdasd dasdasd ipsum ", owner=1))
    db.session.add(Chapter(text="LoremOAKSODKOKASDOKOASKD  ipsum Lorem ipsum Lorem ipsum ", owner=1))
    
    db.session.commit()

@app.route("/", methods=["GET", "POST"])
def base():
    users = User.query.all()
    chapters = Chapter.query.all()
    form = ChapterForm()
    chapter = Chapter()
    if form.validate_on_submit():
        print ("trying to login")
        loggedIn()
        print ("loggedin")
        form.populate_obj(chapter)
        chapter.owner = currentUser().id
        db.session.add(chapter)
        db.session.commit()
        flash("Added a chapter. Thank you.")
        return redirect("/")
        
    return render_template("index.html", chapters=chapters, users=users, form=form)

@app.route("/chapter/<int:id>/edit", methods=["GET", "POST"])
def editChapter(id):
    loggedIn()
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)
    if currentUser().id != chapter.owner:
        abort(403)
    if form.validate_on_submit():
        form.populate_obj(chapter)
        db.session.add(chapter)
        db.session.commit()
        flash("Edited story")
        return redirect("/")
    return render_template("edit.html", form=form)

@app.route("/chapter/<int:id>/delete")
def deleteChapter(id):
    loggedIn()
    chapter = Chapter.query.get_or_404(id)
    if currentUser().id != chapter.owner:
        abort(403)
    return render_template("delete.html", chapter=chapter)

@app.route("/chapter/<int:id>/remove")
def removeChapter(id):
    loggedIn()
    chapter = Chapter.query.get_or_404(id)
    if currentUser().id != chapter.owner:
        abort(403)
    db.session.delete(chapter)
    db.session.commit()
    flash("Deleted a chapter")
    return redirect("/")

if __name__=="__main__":
    app.run()