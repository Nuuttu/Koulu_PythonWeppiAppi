from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def base():
    kissa = "katti"
    return render_template("index.html", kissa=kissa)

@app.route('/double')
def double():
    return render_template("double.html")

@app.route('/triple')
def triple():
    return render_template("triple.html")

if __name__=="__main__":
    app.run(debug=True)