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
    tail = db.Column(db.Boolean, nullable=True)

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

@app.route("/modify/<int:id>", methods=["GET", "POST"])
@app.route("/addAnimal", methods=["GET", "POST"])
def addAnimal(id=None):
    flashmsg = "Added"
    operationMsg = "Add a animal"
    animal = Animal()
    if id:
        animal = Animal.query.get_or_404(id)
        flashmsg = "Modified"
        operationMsg = "Modify animal - " + animal.name
    form = AnimalForm(obj=animal)
    if form.validate_on_submit(): ##
        form.populate_obj(animal)
        db.session.add(animal)
        db.session.commit()
        flash(flashmsg)
        return redirect("/")
    return render_template("addAnimal.html", form=form, operationMsg=operationMsg)

@app.route("/delete/<int:ID>", methods=["GET", "DELETE"]) ###
def deleteAnimal(ID):
    animal = Animal.query.get_or_404(ID)
    db.session.delete(animal)
    db.session.commit()
    flash("Animal deleted :(")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)