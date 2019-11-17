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

from io import BytesIO
import matplotlib.pyplot as plt
import base64
import numpy as np
import pickle


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

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


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div([
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    html.Div(id='output-state'),
    html.Div([html.Img(id = 'cur_plot', src = '')],
             id='plot_div'),
    html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
    ])
])
@app.callback(
    Output('cur_plot', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-1-state', 'value')]
)
def update_graph(n_clicks, input1):
    print(u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks, input1))
    plot_div = long_process(input1)
    return plot_div




@app.callback(
    Output("output-state", "children"),
    [Input("input-1-state", "value")]
)
def update_output(input1):
    return u'Input 1 is {0}'.format(input1)


app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == '__main__':
    app.run_server(debug=True)
