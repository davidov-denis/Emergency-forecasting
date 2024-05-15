from flask import Flask, render_template, request
import database.db as db
import plotly
import plotly.graph_objects as go

app = Flask(__name__)


@app.route("/api/getHeatData/<float:lat_1>/<float:lon_1>/<float:lat_2>/<float:lon_2>")
def getHeatData(lat_1, lon_1, lat_2, lon_2):
    return db.EventInfo().select_points(lat_1, lon_1, lat_2, lon_2)

@app.route("/api/getTypes")
def getTypes():
    return db.EventInfo().select_types()

@app.route("/api/getHeatDataByType/<float:lat_1>/<float:lon_1>/<float:lat_2>/<float:lon_2>")
def getHeatDataByType(lat_1, lon_1, lat_2, lon_2):
    data = request.args.get('types').split(';')
    return db.EventInfo().select_points_by_types(lat_1, lon_1, lat_2, lon_2, data)

@app.route("/api/getHeatData")
def getHeatDataAll():
    return db.EventInfo().select_events_latitude_longitude()


def create_graph(data):
    x = []
    y = []
    for i in data:
        x.append(str(i['hour']) + ":00:00" + '-' + str(i['hour']+1) + ":00:00")
        y.append(i['qty'] / 955)  # среднее количество вызовов в данный промежуток времени в день (955 дней)
    fig = go.Figure(
        data=[go.Bar(y=y, x=x, hoverinfo='text')],
    )
    graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
    return graph_div


@app.route("/analysis/time")
def analytic_time():
    data = db.EventInfo().select_by_time()
    graph_div_time = create_graph(data)
    return render_template("analitic_time.html", data=data, graph_div_time=graph_div_time)

@app.route("/analysis/month")
def analytic_dates():
    data = db.EventInfo().select_by_month()
    return data

@app.route("/map/")
def heat_map():
    return render_template("map.html")


