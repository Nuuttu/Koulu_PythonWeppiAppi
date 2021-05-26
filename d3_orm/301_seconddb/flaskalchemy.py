from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Coffee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String)

@app.before_first_request
def initMe():
    db.create_all()

    db.session.add(Coffee(time=30, amount=2, brand="Saludo"))
    db.session.add(Coffee(time=20, amount=3))
    db.session.add(Coffee(time=15, amount=4, brand="paulig"))
    db.session.commit()

@app.route('/')
def base():
    coffees = Coffee.query.all()

    return render_template("index.html", coffees=coffees)

if __name__=="__main__":
    app.run()