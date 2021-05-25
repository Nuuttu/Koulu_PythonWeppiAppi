from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def base():
    bmi = 0
    if "kg" in request.form and "cm" in request.form:
            kg = int(request.form["kg"])
            cm = int(request.form["cm"])
            bmi = kg / pow((cm/100),2)
    return render_template(
    'index.html',
    bmi=bmi)
    
if __name__=="__main__":
    app.run(debug=True)