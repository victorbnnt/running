# -*- coding: utf-8 -*-

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import os
import requests
from io import BytesIO


app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([





    ])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
