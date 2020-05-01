import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Evert',style={'textAlign':'center'}),
	html.H1(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    html.Div(children='''Step 1: Import data from excel file'''),
	dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Graph(id='Mygraph'),
    html.Div(id='output-data-upload')
])

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@app.callback(Output('Mygraph', 'figure'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
	
def update_graph(contents, filename):
    x = []
    y = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        df = df.set_index(df.columns[0])
        x=df['DATE']
        y=df['TMAX']
    fig = go.Figure(
        data=[
            go.Scatter(
                x=x, 
                y=y, 
                mode='lines+markers')
            ],
        layout=go.Layout(
            plot_bgcolor=colors["graphBackground"],
            paper_bgcolor=colors["graphBackground"]
        ))
    return fig

@app.callback(Output('output-data-upload', 'children'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
		
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])

    return table
	

			


if __name__ == '__main__':
    app.run_server(debug=True)
	
