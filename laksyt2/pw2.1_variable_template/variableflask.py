from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def base():
    kissa = "katti"
    return render_template("index.html", kissa=kissa)

if __name__=="__main__":
    app.run(debug=True)