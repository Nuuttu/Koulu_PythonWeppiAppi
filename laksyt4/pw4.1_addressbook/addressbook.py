from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key="vdpst9JTLe0Q5WtPmqpESKKBm9opFv"
db = SQLAlchemy(app)

class Contact(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=True)
    indebt = db.Column(db.Boolean, nullable=True)

ContactForm = model_form(Contact,
    base_class=FlaskForm, db_session=db.session)

@app.before_first_request
def initDb():
    db.create_all()
    db.session.commit()

@app.route("/")
def base():
    contactlist = Contact.query.all()
    return render_template("index.html", contactlist=contactlist)

@app.route("/modify/<int:id>", methods=["GET", "POST"])
@app.route("/add", methods=["GET", "POST"])
def addContact(id=None):
    flashmsg = "Added"
    operationMsg = "Add Contact"
    contact = Contact()
    if id:
        contact = Contact.query.get_or_404(id)
        flashmsg = "Modified"
        operationMsg = "Modify contact for - " + contact.firstname + " " + contact.lastname
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        form.populate_obj(contact)
        db.session.add(contact)
        db.session.commit()
        flash(flashmsg + " - " + contact.firstname + " " + contact.lastname)
        return redirect("/")
    return render_template("add.html", form=form, operationMsg=operationMsg)

@app.route("/confirmation/<int:id>")
def confirmation(id):
    contact = Contact.query.get_or_404(id)
    return render_template("confirmation.html", contact=contact)

@app.route("/delete/<int:id>", methods=["GET", "DELETE"])
def deleteContact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Deleted - " + contact.firstname + " " + contact.lastname)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)