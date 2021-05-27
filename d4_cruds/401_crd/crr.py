from flask import Flask, render_template, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm # m
from wtforms.ext.sqlalchemy.orm import model_form  # m

app = Flask(__name__)
app.secret_key="72MnJzAnLgLDnTyliXwCDPsRs6BCvB" # m 
db = SQLAlchemy(app) # m

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

MovieForm = model_form(Movie,
    base_class=FlaskForm, db_session=db.session) # m

@app.before_first_request
def initdb():
    db.create_all() # m
    db.session.add(Movie(name="Predator", date="20.02.2021"))
    db.session.add(Movie(name="Whiplash", date="01.03.2021"))
    db.session.add(Movie(name="The Holy Mountain", date="12.04.2021"))
    db.session.commit()

@app.route("/")
def base():
    movies = Movie.query.all() # m
    return render_template("index.html", movies=movies)

@app.route("/add", methods=["GET", "POST"])
def addMovie():
    form = MovieForm()
    if form.validate_on_submit(): # m
        movie = Movie()
        form.populate_obj(movie) # m
        db.session.add(movie)
        db.session.commit()
        flash("added a movie")
        return redirect("/")
    return render_template("add.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)