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
    html.Div(id="data-import-container", className="row", children=[
        html.Div(className="six columns", children=[
            dcc.Upload(id="data-upload"),
        ]),
        html.Div(className="six columns", children=[
            html.Button("Import Data", id="data-import-btn"),
            html.Button("Refresh Plots", id="create-plots-btn")
        ])
    ]),

    # Main tabs
    dcc.Tabs(id="main-tabs", value="transaction-explorer", children=[
        dcc.Tab(label="Transactions Overview", value="transactions-overview", id="transactions-overview"),
        dcc.Tab(label="Month Breakdown", value="month-breakdown"),
        dcc.Tab(label="Explorer", value="transaction-explorer", children=[
            html.Div(className="row", children=[
                html.Div(className="four columns", children=[
                    html.P("Date Range"),
                    dcc.DatePickerRange(id="explorer-date-picker")
                ]),
                html.Div(className="four columns", children=[
                    html.P("Accounts"),
                    dcc.Checklist(id="explorer-accounts-selector", options=[], values=[])
                ]),
                html.Div(className="four columns", children=[
                    html.P("Transaction Type"),
                    dcc.Checklist(id="explorer-type-selector", options=[
                        {"label": "Debit", "value": "debit"},
                        {"label": "Credit", "value": "credit"}
                    ], values=["debit", "credit"])
                ]),
            ]),
            html.Div(className="row", children=[
                html.Div(className="four columns", children=[
                    html.P("Category"),
                    dcc.Dropdown(id="explorer-category-selector", options=[{"label": "All", "value": "All"}]+[{"label": i, "value": i} for i in visualizer.get_category_list()], value=["All"], multi=True)
                ]),
                html.Div(className="four columns", children=[
                    html.P("Subcategory"),
                    dcc.Dropdown(id="explorer-subcategory-selector", options=[{"label": "All", "value": "All"}]+[{"label": i, "value": i} for i in visualizer.get_subcategory_list()], value=["All"], multi=True)
                ]),
                html.Div(className="four columns", children=[
                    html.P("Merchants"),
                    dcc.Dropdown(id="explorer-merchant-selector", options=[], value=[], multi=True)
                ])
            ]),
            html.Div(id="explorer-btn-container", className="row", children=[
                html.Button("Submit", id="explorer-submit-btn")
            ]),
            html.Div(className="row", id="explorer-plot")
        ])
    ]), # End tabs

]) # End of app layout


@app.callback(Output(component_id="data-upload", component_property="children"),
        [Input(component_id="data-import-btn", component_property="n_clicks")],
        [State(component_id="data-upload", component_property="contents"),
        State(component_id="data-upload", component_property="filename")])
def display_transactions(n_clicks, contents, filename):
    children = html.Div([
                    html.A("Select Mint Transactions File"),
                ])
    if n_clicks is None:
        return children

    if filename is None:
        return children

    df = util.parse_content(contents, filename)
    visualizer.set_transaction_data(df)
     
    children = [html.Div(children=[
            html.P(f"Successfully uploaded {filename}."),
            html.A("Click here to select a different file."),
        ])]
    return children


@app.callback(Output(component_id="transactions-overview", component_property="children"),
        [Input(component_id="create-plots-btn", component_property="n_clicks")])
def plot_overview(n_clicks):
    if n_clicks is None:
        return html.P("Upload data to see transactions overview")
    
    children = [
        html.Div(className="row", children=[
            html.Div(className="six columns", children=[
                dcc.Graph(figure=visualizer.plot_agreggate_transactions_by_month())
            ]),
            html.Div(className="six columns", children=[
                dcc.Graph(figure=visualizer.plot_category_pie())
            ])
        ])
    ]
    return children


@app.callback([Output(component_id="explorer-accounts-selector", component_property="options"),
               Output(component_id="explorer-accounts-selector", component_property="values")],
              [Input(component_id="data-import-btn", component_property="n_clicks")])
def update_explorer_accounts_options(n_clicks):
    default = [], []
    if n_clicks is None:
        return default
    accounts_list = visualizer.get_accounts_list()
    
    if accounts_list is None:
        return default
    
    options = [{"label": i, "value": i} for i in accounts_list]
    return options, accounts_list


@app.callback([Output(component_id="explorer-merchant-selector", component_property="options"),
               Output(component_id="explorer-merchant-selector", component_property="value")],
              [Input(component_id="data-import-btn", component_property="n_clicks")])
def update_explorer_merchant_options(n_clicks):
    default = [], []
    if n_clicks is None:
        return default
    merchant_list = visualizer.get_merchant_list()
    
    if merchant_list is None:
        return default
    
    options = [{"label": "All", "value": "All"}] + [{"label": i, "value": i} for i in merchant_list]
    return options, ["All"]


@app.callback([Output(component_id="explorer-date-picker", component_property="min_date_allowed"),
               Output(component_id="explorer-date-picker", component_property="max_date_allowed"), 
               Output(component_id="explorer-date-picker", component_property="initial_visible_month"),
               Output(component_id="explorer-date-picker", component_property="start_date"),
               Output(component_id="explorer-date-picker", component_property="end_date")],
              [Input(component_id="data-import-btn", component_property="n_clicks")])
def update_explorer_accounts_options(n_clicks):
    default_min = dt.date(2016, 1, 1)
    default_max = dt.date.today()
    initial_visible_month = dt.date.today()
    start_date = default_min
    end_date = default_max
    if n_clicks is None:
        return default_min, default_max, initial_visible_month, start_date, end_date
    
    date_range = visualizer.get_date_range()
    if date_range is None:
        return default_min, default_max, initial_visible_month, start_date, end_date
    
    start_date = date_range[0]
    end_date = date_range[1]
    return start_date, end_date, initial_visible_month, start_date, end_date
    

@app.callback(Output(component_id="explorer-plot", component_property="children"),
             [Input(component_id="explorer-submit-btn", component_property="n_clicks")],
             [State(component_id="explorer-date-picker", component_property="start_date"),
              State(component_id="explorer-date-picker", component_property="end_date"),
              State(component_id="explorer-accounts-selector", component_property="values"),
              State(component_id="explorer-type-selector", component_property="values"),
              State(component_id="explorer-category-selector", component_property="value"),
              State(component_id="explorer-subcategory-selector", component_property="value"),
              State(component_id="explorer-merchant-selector", component_property="value")
             ])
def update_explorer_plot(n_clicks, start_date, end_date, accounts, transaction_types, categories, subcategories, merchants):
    children = html.Div("Enter options and click Submit")
    if n_clicks is None:
        return children
    
    if "All" in categories:
        categories = None
    if "All" in subcategories:
        subcategories = None
    if "All" in merchants:
        merchants = None
    
    children = html.Div(children=[
        dcc.Graph(figure=visualizer.plot_explorer(start_date, end_date, accounts, transaction_types, categories, subcategories, merchants))
    ])
    
    return children


if __name__ == "__main__":
    app.run_server(debug=True)
    # import os
    # app.run_server(host=os.environ["IP"], port=os.environ["PORT"], debug=True)
    # http://mint-finance-dashboard-aadelucia.c9users.io
