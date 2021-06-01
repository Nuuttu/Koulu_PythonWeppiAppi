from flask import Flask, render_template, redirect, flash, session, abort, request
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, validators, SubmitField
from datetime import datetime

app = Flask(__name__)
app.secret_key="cvhQr6otEjf8O8YdSO6U7liDu6ycoz"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, foreign_key="User.id")
    roomId = db.Column(db.Integer, foreign_key=True, nullable=True)
    task = db.Column(db.String, nullable=False)
    c_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

TodoForm = model_form(Todo, base_class=FlaskForm, db_session=db.session, exclude = ["userId", "roomId", "c_date"])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    passwordHash = db.Column(db.String, nullable=False)

    def setPassword(self, password):
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    

class UserForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email()])
    password = PasswordField("Password", validators=[validators.InputRequired()])

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[validators.Email()])
    password = PasswordField("Password", validators=[validators.InputRequired()])
    registerKey = StringField("Registration Key", validators=[validators.InputRequired()])

#rooms = db.Table("rooms",
#    db.Column("room_id", db.Integer, db.ForeignKey("room.id"), primary_key=True),
#    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
#)
############################ under construction


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"))

class RoomForm(FlaskForm):
    name = StringField("Create a room: ", validators=[validators.InputRequired()])
    
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, foreign_key=True, nullable=False)
    room_id = db.Column(db.Integer, foreign_key=True, nullable=False)

##########################################################################################
##########################################################################################
##########################################################################################
class MemberForm(FlaskForm):
    userName = StringField("name a new member: ", validators=[validators.InputRequired()])
    submit = SubmitField('submit')

    def setUser(self, user):
        self.user_id = User.query.filter_by(name=name).first()
        
    def setRoom(self, roomid):
        self.room_id = Room.query.get_or_404(roomid)

    #members = db.Column("myarray", ARRAY(Integer))
    #rooms = db.relationship("room", secondary=rooms, lazy="subquery", backref=db.backref('rooms', lazy=True))
############################ under construction



## CurrentUser config

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

def currentRoom():
    try:
        rid = int(session["rid"])
    except:
        return None
    return Room.query.get(rid)

app.jinja_env.globals["currentRoom"] = currentRoom

#def inRoom():
#    if not currentRoom():
#        return abort(403)


## user view

@app.route("/register", methods=["GET", "POST"])
def registerUser():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        registerKey = form.registerKey.data

        if User.query.filter_by(email=email).first():
            flash("User already exist. Log in")
            return redirect("/login")
        if not registerKey == "cube":
            flash("Wrong register key. You need to know this in order to register.")
            return redirect("/register")
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
        flash("Login success. Hello " + currentUser().email)
        return redirect("/")
        
    return render_template("login.html", form=form)


@app.route("/logout")
def logoutUser():
    session["uid"] = None
    session["rid"] = None
    flash("Logged out.")
    return redirect("/")


## Rooms view


@app.route("/joinroom/<int:id>", methods=["GET", "POST"])
def joinRoom(id):
    loggedIn()
    
    session["rid"]=id
    flash("Join room success. You are now in " + currentRoom().name)
    return redirect("/")
        
    return render_template("joinroom.html")


@app.route("/leaveroom")
def leaveRoom():
    session["rid"] = None
    flash("Left room")
    return redirect("/")



## Before First Request

@app.before_first_request
def initDb():
    db.create_all()
    db.session.add(Todo(task="Run", userId=1))
    db.session.add(Todo(task="All I Need", userId=1, roomId=1))
    db.session.add(Todo(task="All", userId=2, roomId=1))
    db.session.add(Room(name="First Room", owner=1))
    db.session.add(Room(name="Second Room", owner=2))
    user = User(email="asd@asd.asd")
    user.setPassword("asd")
    db.session.add(user)
    user = User(email="qwe@qwe.qwe")
    user.setPassword("qwe")
    db.session.add(user)
    user = User(email="zxc@zxc.zxc")
    user.setPassword("zxc")
    db.session.add(user)
    db.session.commit()


## Main view

@app.route("/")
def base():
    helloMessage = "Hello, please login or register for Tasks and Todos!"
    if currentUser():
        todos = Todo.query.filter_by(userId=currentUser().id)
        if Todo.query.filter_by(userId=currentUser().id).count() == 0:
            return render_template("index.html")
        else:
            return render_template("index.html", todos=todos)
    return render_template("index.html")
#### form.request add_member

@app.errorhandler(404)
def custom404(e):
    return render_template("404.html")

@app.errorhandler(403)
def custom403(e):
    flash("You need to log in to do this.")
    return redirect("/")


@app.route("/rooms", methods=["GET", "POST"])
def rooms(ID=None):
    loggedIn()
    room = Room()
    form = RoomForm()
    if form.validate_on_submit():
        form.populate_obj(room)
        room.owner = currentUser().id
        if Room.query.filter_by(name=room.name).first():
            flash("Room in use. Use different name.")
            return redirect("/rooms")
        db.session.add(room)
        db.session.commit()
    if "joinroom" in request.form:
        if not Room.query.filter_by(name=request.form["joinroom"]).first():
            flash("Can't find that room")
            return redirect("/rooms")
        roomname = request.form["joinroom"]
        print (roomname + "...")
        room = Room.query.filter_by(name=roomname).first()
        roomtojoin = "/joinroom/" + str(room.id)
        return redirect(roomtojoin)
    rooms = Room.query.filter_by(owner=currentUser().id)
    ##########################################################################################
    ##########################################################################################
    ##########################################################################################
    memberform = MemberForm()
    if memberform.validate_on_submit() and currentRoom():
        member = Member()
        newMember = User.query.filter_by(name=memberform.name).first()
        member.setUserId(newMember.id)
        member.serRoomId(currentRoom().id)
        db.session.add(member)
        db.session.commit()
        flash("added member to this room")
        return redirect("/rooms")
    return render_template("rooms.html", rooms=rooms, form=form, memberform=memberform)

@app.route("/rooms/delete/<int:id>")
def deleteRoom(id):
    loggedIn()
    room = Room.query.get_or_404(id)
    if currentUser().id != room.owner:
        abort(403)    
    return render_template("deleteroom.html", room=room)
    

@app.route("/rooms/remove/<int:id>")
def removeRoom(id):
    loggedIn()
    room = Room.query.get_or_404(id)
    if currentUser().id != room.owner:
        abort(403)
    db.session.delete(room)
    db.session.commit()
    flash("Deleted room")
    return redirect("/rooms")


@app.route("/todo/<int:id>/edit", methods=["GET", "POST"])
@app.route("/todo/add", methods=["GET", "POST"])
def addTodo(id=None):
    if not currentUser():
        abort(403)
    todo = Todo()
    todo.userId = currentUser().id
    if currentRoom():
        todo.roomId = currentRoom().id
    message = "Add a new Todo"
    flashmessage = "Added Todo: "
    pageTitle = "Add Todo"
    if id:
        todo = Todo.query.get_or_404(id)
        if currentUser().id != todo.userId:
            abort(403)  
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
    loggedIn()
    todo = Todo.query.get_or_404(id)
    if currentUser().id != todo.userId:
        abort(403)    
    return render_template("delete.html", todo=todo)
    

@app.route("/<int:id>/annihilate")
def annihilateTodo(id):
    loggedIn()
    todo = Todo.query.get_or_404(id)
    if currentUser().id != todo.userId:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash("Deleted todo: - " + todo.task)
    return redirect("/")

    
    
if __name__ == "__main__":
    app.run(debug=True)
