
from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

CSV = Path(__file__).parent / "spacex_launch_dash.csv"
df = pd.read_csv(CSV)
site_col = "Launch Site"
payload_col = "Payload Mass (kg)"
class_col = "class"
booster_col = "Booster Version Category" if "Booster Version Category" in df.columns else None

app = Dash(__name__)
sites = sorted(df[site_col].dropna().unique())
options = [{"label":"All Sites","value":"ALL"}] + [{"label":s,"value":s} for s in sites]
payload_min = int(df[payload_col].min() // 1000 * 1000)
payload_max = int((df[payload_col].max() // 1000 + 1) * 1000)

app.layout = html.Div([
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign":"center"}),
    html.Label("Launch Site"),
    dcc.Dropdown(id="site-dropdown", options=options, value="ALL", clearable=False),
    dcc.Graph(id="success-pie-chart"),
    html.Label("Payload range (kg)"),
    dcc.RangeSlider(id="payload-slider", min=payload_min, max=payload_max, step=1000,
                    value=[payload_min,payload_max], marks={v:str(v) for v in range(payload_min,payload_max+1, max(1000,(payload_max-payload_min)//5 or 1000))}),
    dcc.Graph(id="success-payload-scatter-chart")
], style={"fontFamily":"Arial","margin":"2rem"})

@app.callback(Output("success-pie-chart","figure"), Input("site-dropdown","value"))
def update_pie(site):
    data = df if site == "ALL" else df[df[site_col] == site]
    if site == "ALL":
        summary = data.groupby(site_col)[class_col].sum().reset_index()
        return px.pie(summary, values=class_col, names=site_col, title="Successful Launches by Site")
    counts = data[class_col].value_counts().reindex([0,1], fill_value=0).rename_axis("Outcome").reset_index(name="Count")
    counts["Outcome"] = counts["Outcome"].map({0:"Failure",1:"Success"})
    return px.pie(counts, values="Count", names="Outcome", title=f"Outcomes at {site}")

@app.callback(Output("success-payload-scatter-chart","figure"),
              Input("site-dropdown","value"), Input("payload-slider","value"))
def update_scatter(site, payload_range):
    data = df[df[payload_col].between(payload_range[0],payload_range[1])]
    if site != "ALL":
        data = data[data[site_col] == site]
    color = booster_col if booster_col else site_col
    return px.scatter(data, x=payload_col, y=class_col, color=color, hover_data=[site_col],
                      title="Payload Mass vs Mission Outcome",
                      labels={payload_col:"Payload Mass (kg)",class_col:"Mission outcome"})

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
