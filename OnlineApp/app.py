import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


image_filename = "figures/boxplot.png" # replace with your own image
test_base64 = base64.b64encode(open(image_filename, 'rb').read())

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig = open("figures/boxplot.png")
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


app.layout = html.Div(children=[
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
    ),
    html.Img(src=app.get_asset_url('figures/boxplot.png')),
    #html.Div([html.Img(id = 'cur_plot', src = '')],
    #         id='plot_div')
    html.Img(src='data:image/png;base64,{}'.format(test_base64))

])

if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True, port=8050)
    #app.run_server(host=‘0.0.0.0’,debug=True, port=8050)
