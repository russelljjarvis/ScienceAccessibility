import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html

import datetime
import time
from SComplexity import online_app_backend
from SComplexity.OnlineApp import bplot

import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

class Semaphore:
    def __init__(self, filename='semaphore.txt'):
        self.filename = filename
        with open(self.filename, 'w') as f:
            f.write('done')

    def lock(self):
        with open(self.filename, 'w') as f:
            f.write('working')

    def unlock(self):
        with open(self.filename, 'w') as f:
            f.write('done')

    def is_locked(self):
        return open(self.filename, 'r').read() == 'working'


semaphore = Semaphore()


def long_process(NAME):
    if semaphore.is_locked():
        raise Exception('Resource is locked')
    semaphore.lock()
    NAME = "S S Phatak"
    verbose = True
    #verbose = False
    #import pdb
    #pdb.set_trace()
    ar = online_app_backend.call_from_front_end(NAME,verbose=verbose)
    print(ar)
    axes,fig = bplot.plot_author(ar,NAME)

    semaphore.unlock()
    return axes,fig



app = dash.Dash()
server = app.server


def layout():
    return html.Div([
        html.Button('Run Process', id='button'),
        dcc.Interval(id='interval', interval=500),
        html.Div(id='lock'),
        html.Div(id='output'),
    ])


app.layout = layout


@app.callback(
    Output('lock', 'children'),
    events=[Event('interval', 'interval')])
def display_status():
    return 'Running...' if semaphore.is_locked() else 'Free'


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
    html.Div([html.Img(id = 'cur_plot', src = '')],
             id='plot_div')
])





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])

'''
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
'''
@app_iplot.callback(
    Output(component_id='cur_plot', component_property='src'),
    [Input(component_id='plot_title', component_property='value'), Input(component_id = 'box_size', component_property='value')]
)
def update_output_div(input_value):
    print('You\'ve entered "{0}, searching for that author now..."'.format(input_value))
    axes,fig = long_process(input_value)
    out_url = fig_to_uri(fig)
    return out_url
'''
def update_graph(input_value, n_val):
    out_url = fig_to_uri(fig)
    return out_url
'''    


if __name__ == '__main__':
    app.run_server(debug=True, processes=5)
