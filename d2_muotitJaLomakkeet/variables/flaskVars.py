from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    siteTitle = 'siteIndex'
    name = 'Tuomo'
    listOfThings = ['A thing', 'The Thing', 'Thing', 'A Big Thing']
    return render_template('base.html', 
    name=name, 
    siteTitle=siteTitle,
    listOfThings=listOfThings)

@app.route('/child')
def child():
    siteTitle = 'Child page'
    return render_template('child.html', siteTitle=siteTitle)

if __name__ == '__main__':
    app.run(debug=True)