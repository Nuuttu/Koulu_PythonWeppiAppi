from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def base():
    cars = ['ferrari', 'maserati', 'mclaren']
    bikes = []
    number = 0
    title = ""
    return render_template(
    'base.html', 
    cars=cars, 
    bikes=bikes, 
    number=number,
    title=title)
    
if __name__=="__main__":
    app.run(debug=True)