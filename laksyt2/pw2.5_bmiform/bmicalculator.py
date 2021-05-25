from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
@app.route('/result', methods=["GET", "POST"])
def base():
    page = "index.html"
    bmi = 0
    if "kg" in request.form and "cm" in request.form:
            kg = int(request.form["kg"])
            cm = int(request.form["cm"])
            bmi = kg / pow((cm/100),2)
            page = request.form["newpage"]
    return render_template(
    page,
    bmi=bmi)


    
if __name__=="__main__":
    app.run(debug=True)