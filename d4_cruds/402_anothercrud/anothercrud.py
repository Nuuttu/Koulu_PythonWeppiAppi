from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm #
from wtforms.ext.sqlalchemy.orm import model_form #

app = Flask(__name__)
app.secret_key="vdpst9JTLe0Q5WtPmqpESKKBm9opFv"
db = SQLAlchemy(app) #

class Animal(db.Model): #
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    numberOfLegs = db.Column(db.Integer, nullable=False)
    tail = db.Column(db.Boolean, nullable=False)

AnimalForm = model_form(Animal,
    base_class=FlaskForm, db_session=db.session) ####

@app.before_first_request
def initDb():
    db.create_all()
    db.session.add(Animal(name="Dog", numberOfLegs=4, tail=True))
    db.session.commit()

@app.route("/")
def base():
    animals = Animal.query.all()
    return render_template("index.html", animals=animals)

@app.route("/addAnimal", methods=["GET", "POST"])
def addAnimal():
    form = AnimalForm()
    if form.validate_on_submit(): ##
        animal = Animal()
        form.populate_obj(animal)
        db.session.add(animal)
        db.session.commit()
        flash("Added")
        return redirect("/")
    return render_template("addAnimal.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)