# -*- coding: utf-8 -*-

import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os
import requests
from io import BytesIO
from functions.compute import CourseAPied
import pandas as pd


m = CourseAPied("My running sessions")
my_running_sessions = m.data_from_csv("data_course_a_pied.csv")
#my_running_sessions["Date"] = pd.to_datetime(my_running_sessions["Date"], format='%d/%m/%Y')

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Convert the DataFrame to a dictionary format
data = my_running_sessions.tail().to_dict('records')

# Create a Dash table component
table = dash_table.DataTable(
    columns=[{'name': i, 'id': i} for i in my_running_sessions.columns],
    data=data,
    style_as_list_view=True
)
app.layout = dbc.Container([dcc.Location(id='BRU', refresh=False),
                            html.Div(children=[html.H1('Running tracker',style={"color": "white", "font-family":"sans-serif","padding-top":"10px","padding-bottom":"10px"})],
                                     style={"display": "block","textAlign": "center","backgroundColor": "#1E1E1E"}
                                    ),
                            html.Div(children=[table],style={"width":"100%","display":"block","margin":"auto","font-size":"12pt"})
                            ])



if __name__ == '__main__':
    print(my_running_sessions.tail())
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
