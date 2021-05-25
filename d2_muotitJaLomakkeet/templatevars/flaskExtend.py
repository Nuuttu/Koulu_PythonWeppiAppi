from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def base():
    name = "Tuomo"
    return render_template('base.html', name=name)

@app.route('/index')
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)