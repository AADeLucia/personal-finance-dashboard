import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import datetime as dt
from visualizer import Visualizer
from utility import Utility

visualizer = Visualizer()
util = Utility()

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
        html.Button("Import Data", id="data-import-btn"),
        html.Button("Refresh Plots", id="create-plots-btn", disabled="True")
    ]),

    # Main tabs
    dcc.Tabs(id="main-tabs", value="transactions-overview", children=[
        dcc.Tab(label="Transactions Overview", value="transactions-overview", children=[
            html.Div(className="row", children=[
                html.Div(className="six columns", id="month-overview", children=[
                    html.P("Number of Transactions by Month"),
                ]),
            ]),
        ]),
        dcc.Tab(label="Month Breakdown", value="month-breakdown")
    ]), # End tabs

]) # End of app layout


@app.callback(Output(component_id="file-status", component_property="children"),
        [Input(component_id="data-import-btn", component_property="n_clicks")],
        [State(component_id="data-upload", component_property="contents"),
        State(component_id="data-upload", component_property="filename")])
def display_transactions(n_clicks, contents, filename):
    if n_clicks is None:
        return

    if filename is None:
        return "No file selected"

    df = util.parse_content(contents, filename)
    visualizer.set_transaction_data(df)
    return f"Successfully uploaded {filename}"


@app.callback(Output(component_id="create-plots-btn", component_property="disabled"),
        [Input(component_id="data-import-btn", component_property="n_clicks")],
        [State(component_id="data-upload", component_property="contents"),
        State(component_id="data-upload", component_property="filename")])
def enable_button(n_clicks, contents, filename):
    if n_clicks is None:
        return "True"

    if filename is None:
        return "True"

    return "False"


@app.callback(Output(component_id="month-overview", component_property="children"),
        [Input(component_id="create-plots-btn", component_property="n_clicks")])
def plot_month_overview(n_clicks):
    print("here")
    if n_clicks is None:
        return html.P("Upload data to see month overview")
    print("Recognized click")
    return dcc.Graph(figure=visualizer.plot_agreggate_transactions_by_month())


if __name__ == "__main__":
    app.run_server(debug=True)
