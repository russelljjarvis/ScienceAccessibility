import dash
from dash.dependencies import Input, Output#, Event
import dash_core_components as dcc
import dash_html_components as html
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


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
    if semaphore.is_locked():
        raise Exception('Resource is locked')
    semaphore.lock()
    time.sleep(7)
    semaphore.unlock()
    #return
    print('enters long process')
    #NAME = "S S Phatak"
    verbose = True

    ar = online_app_backend.call_from_front_end(NAME,verbose=verbose)
    print(ar)

    axes,fig = bplot.plot_author(ar,NAME)

    semaphore.unlock()
    return axes,fig


app = dash.Dash()
server = app.server


# app.layout = layout
'''
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div([
        html.Button('Run Process', id='button'),
        dcc.Interval(id='interval', interval=500),
        html.Div(id='lock'),
        html.Div(id='output'),
    ]),
    html.Div(children=
        Dash: A web application framework for Python.
    ),


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
    )])


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

@app_iplot.callback(
    Output(component_id='cur_plot', component_property='src'),
    [Input(component_id='plot_title', component_property='value'), Input(component_id = 'box_size', component_property='value')]
)
'''
def update_graph(input_value, n_val):

    out_url = fig_to_uri(fig)
    return out_url


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(id='target'),
    dcc.Input(id='input', type='text', value='Enter Author Name here, with the name formated as you would a google scholar search'),
    html.Button(id='submit', type='submit', children='ok'),
    dcc.Interval(id='interval', interval=500),
    html.Div(id='output'),
])


@app.callback(
    Output('lock', 'children'),
    events=[Event('interval', 'interval')])
def display_status():
    return 'Running long job in background please wait {0}'.format(datetime.datetime.now()) if semaphore.is_locked() else 'Free'


#def layout():
#    return html.Div([
#        html.Button('Run Process', id='button'),
#    ])




#app.layout = html.Div([
#    dcc.Input(id='my-id', value='Enter Author Name here, with the name formated as you would a google scholar search', type='text'),
#    html.Button(id='submit', type='submit', children='ok'),
#    html.Div(id='my-div')
#])


#@app.callback(
    #Output(component_id='my-div', component_property='children'),
    #[Input(component_id='my-id', component_property='value')]
#)

@app.callback(
    Output('target', 'children'), [], [State('input', 'value')], [Event('submit', 'click')]
)
def callback(state):
    return "callback received value: {}".format(state)


#import time
def update_output_div(input_value):
    print('main loop')
    print('You\'ve entered "{0}, searching for that author now..."'.format(input_value))
    #print(time.time)
    axes,fig = long_process(input_value)
    print('gets here \n\n\n')
    plot_url = py.plot_mpl(fig)
    plot_div = html.Div([
    dcc.Graph(
        id='3D_plot',
        figure = {plot_url
        }
    )
    ])
    return plot_div

#plot_url = py.plot_mpl(fig)
#Would I then call the “plot_url” object in my dash app? For example:

#app.layout =

    return


if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True, port=8050)
    # app.run_server(host='127.0.0.1',port=8050)#debug=True)
#  http://127.0.0.1:8050/
