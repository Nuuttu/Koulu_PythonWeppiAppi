from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def itseApp():
    return render_template("base.html",
     message="this is a message")

@app.route('/plus')
def plus():
    return render_template("base.html", 
    message="plus plus")

if __name__ == '__main__':
    app.run(debug=True)