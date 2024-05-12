import plotly
import plotly.graph_objects as go

fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
)
graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
print(graph_div)
