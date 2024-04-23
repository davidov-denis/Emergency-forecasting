from flask import Flask, render_template
import database.db as db

app = Flask(__name__)


@app.route("/api/getHeatData/")
def getHeatData():
    return db.EventInfo().select_events_latitude_longitude()


@app.route("/map/")
def heat_map():
    return render_template("map.html")


app.run(debug=True)
