# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pickle
import plotly.express as px
import pandas as pd
import numpy as np
import datetime
import time
# get wikipedia data
with open('scraped_new.p','rb') as f:
    texts = pickle.load(f)

queries = set([t['query'] for t in texts ])
temp = [t for t in texts if 'standard' in t.keys() and 'wikipedia' in t['link']]
science = ['cancer','Vaccines','evolution','climate change','Transgenic','photosysnthesis','evolution','GMO']
res = [t['standard'] for t in temp if t['query'] in science]
mwp = np.mean(res)
abstract_wiki = {'standard':mwp}

def new_old(old,new):
    old['Art_Corpus_Derived'] = True
    new['Art_Corpus_Derived'] = False
    newer = old.append(new)
    return newer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def long_process(NAME):
    with open('traingDats.p','rb') as f:
        artcorpus = pickle.load(f)
    with open('scraped_new.p','rb') as f:
        new_author = pickle.load(f)

    new_author = pd.DataFrame(new_author)
    artcorpus = pd.DataFrame(artcorpus)

    print('enters long process')
    verbose = True
    # compute expensive code that I really want to use.
    # import online_app_backend
    # from SComplexity import online_app_backend
    # ar = online_app_backend.call_from_front_end(NAME,verbose=verbose)
    newer = new_old(artcorpus,ar)
    plot = dcc.Graph(
        id='example-graph',
        figure = px.histogram(newer, x="standard", y="standard", color="Art_Corpus_Derived",
                   marginal="box", # or violin, rug
                   hover_data=newer.columns,width=900, height=900)
    )
    return plot

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    dcc.Input(id='input-1-state', type='text', value='enter author name'),
    html.Div(id='newer'),
    html.Div([html.Img(id = 'long_process', src = '')],
             id='plot_div'),
    html.H1(children='Author contest on science readability'),
    html.Div(children='''
        Wikipedia on science, versus art corpus all biochem papers.
    ''')
])
@app.callback(
    Output('newer', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-1-state', 'value')]
)
def update_graph(n_clicks, value):
    print(u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks))
    print(u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(value))
    newer = long_process(value)
    return newer

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
if __name__ == '__main__':
    app.run_server(debug=True)
