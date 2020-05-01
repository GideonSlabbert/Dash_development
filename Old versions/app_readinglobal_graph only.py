import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


df1 = pd.read_csv('parsed_data.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    dcc.Graph(id='Mygraph'),
	html.Button(id='submit-button-state',n_clicks = 0, children='Submit')
])
	   

	
#df = parse_data(contents, filename)

			   
@app.callback(Output('Mygraph', 'figure'),
            [Input('submit-button-state', 'n_clicks')])
def update_graph(n_clicks):
    fig = {
        'layout': go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"])
    }


    df = df1
    df = df.set_index(df.columns[0])
    fig = df.iplot(asFigure=True, kind='scatter', mode='lines+markers', size=1)

	
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)