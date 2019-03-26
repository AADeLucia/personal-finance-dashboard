import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import datetime as dt


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Finance Dashboard"
app.layout = html.Div(children=[
    html.H1("Personal Finance Dashboard"),

    # Data import
    html.Div(id="data-import", children=[
        dcc.Upload(id="data-upload", children=[
            html.Div([
                html.A("Select Mint Transactions File"),
            ]),
        ]),
        html.Div(id="file-status"),
        html.Button("Import Data", id="data-import-btn")
    ])
])


@app.callback(Output(component_id="file-status", component_property="children"),
        [Input(component_id="data-import-btn", component_property="n_clicks")]
        [State(component_id="data-upload", component_property="contents"),
        State(component_id="data-upload", component_property="filename")])
def display_transactions(n_clicks, contents, filename):
    if n_clicks > 0:
        return f"Successfully uploaded {filename}"
    else:
        return "No file selected"


if __name__ == "__main__":
    app.run_server(debug=True)
