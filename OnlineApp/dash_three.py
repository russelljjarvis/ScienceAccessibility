# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


import datetime
import time
try:
    import bplot
    import online_app_backend
except:
    from SComplexity import online_app_backend
    from SComplexity.OnlineApp import bplot

import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64



def long_process(NAME):

    #return
    print('enters long process')
    #NAME = "S S Phatak"
    verbose = True

    ar = online_app_backend.call_from_front_end(NAME,verbose=verbose)
    print(ar)

    axes,fig = bplot.plot_author(ar,NAME)
    out_url = fig_to_uri(fig)
    return out_url

#def update_graph(input_value, n_val):

#    out_url = fig_to_uri(fig)
#    return out_url


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app_iplot = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app_iplot.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    html.Div([html.Img(id = 'cur_plot', src = '')],
             id='plot_div')
])
'''
app_iplot = dash.Dash()

app_iplot.layout = html.Div([
    dcc.Input(id='plot_title', value='Type title...', type="text"),
    dcc.Slider(
        id='box_size',
        min=1,
        max=10,
        value=4,
        step=1,
        marks=list(range(0, 10))
    ),

])
'''
#@app.callback(Output('output-state', 'children'),
#              [Input('submit-button', 'n_clicks')],
#              [State('input-1-state', 'value')])
@app_iplotly.callback(
    Output('output-state', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('input-1-state', 'value')],
    Output(component_id='cur_plot', component_property='figure'),
    [Input(component_id='cur_plot', component_property='clickData')]
)
def update_output(n_clicks, input1):
    print(u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks, input1))
    out_url = long_process(input1)
    return out_url




if __name__ == '__main__':
    app.run_server(debug=True)
