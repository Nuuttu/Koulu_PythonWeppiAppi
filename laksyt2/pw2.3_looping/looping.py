from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def base():
    kissaRotuja = ["Maatiainen", 
    "Ullakkokissa", 
    "Pitkäkarvainen", 
    "Egyptiläinen"]
    return render_template("index.html", kissaRotuja=kissaRotuja)

@app.route('/double')
def double():
    koirarotuja = ["Villakoira",
    "Kultainennoutaja",
    "Saksanpaimen",
    "Espanjalainen vesikoira"]
    return render_template("double.html", koirarotuja=koirarotuja)
    
if __name__=="__main__":
    app.run(debug=True)