from flask import Flask, render_template, flash, redirect


app=Flask(__name__)
app.secret_key="HpoV3oeD9lFNJEvUz2t4Bm6xtvWe4k"

@app.route('/flashing')
def flashing():
    flash("FLASH", "flashone")
    return redirect('/')

@app.route('/flashtwo')
def flashtwo():
    flash("Other Flash", "flashtwo")
    return redirect('/')

@app.route('/')
def base():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)