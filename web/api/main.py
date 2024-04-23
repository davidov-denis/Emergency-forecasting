from flask import Flask, render_template

app = Flask(__name__)


@app.route("/api/getHeatData/")
def getHeatData():
    return [[48.7194, 44.5018], [48.7195, 44.5017]]


@app.route("/map/")
def heat_map():
    return render_template("map.html")


app.run(debug=True)
