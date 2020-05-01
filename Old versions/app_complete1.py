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

df = pd.DataFrame()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(children='Visual Analytic System',style={'textAlign':'center'}),
	html.H1(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    html.Div(children='''Step 1: Import data from excel/csv/textfile file'''),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '35px',
            'lineHeight': '35px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
              },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Button(id='process-data',n_clicks = 0, children='Process the selected files',
                style={'width': '100%'}),     
    dcc.Graph(id='Mygraph',
              style={
                      'width': '100%',
                      'borderRadius': '5px',
                      'borderWidth': '1px',
                      'height': '350px',
                      'paper_bgcolor':'#FFFFFF',
                      'plot_bgcolor':'#FFFFFF'     
                      }),
    html.Div(id='output-data-upload')
])


	   
def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
	
    decoded = base64.b64decode(content_string)
	
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
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
	
#df = parse_data(contents, filename)

			   
@app.callback(Output('Mygraph', 'figure'),
            [Input('process-data', 'n_clicks')],
                [State('upload-data', 'contents'),
                State('upload-data', 'filename')
            ])
def update_graph(n_clicks,contents, filename):
#    fig = {
#        'layout': go.Layout(
#            plot_bgcolor=colors["graphBackground"],
#            paper_bgcolor=colors["graphBackground"])
#    }
    fig = go.Figure()
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
		
        df = df.set_index(df.columns[0])
        
        y_index = 1
        for value in df.iteritems():
            fig.add_trace(
                    go.Scattergl(
									x = df.index,
									y = value[1]
									,name = value[0]
									,yaxis = 'y'+str(y_index)
								)
			)
            fig['layout'].update({
									'yaxis{}'.format(y_index):dict(
                                                             visible = False,
                                                             autorange = True
                                                             )
								 })
            y_index += 1
				
        fig.update_layout(xaxis_showgrid=False, 
                          yaxis_showgrid=False,
                          margin=dict(l=10, r=10, t=10, b=20)
                          ,paper_bgcolor="#FFFFFF"
                          ,plot_bgcolor="#FFFFFF"
                          )
        
        fig.update_traces(
                            line=dict(width=1),
                            marker=dict(opacity=1)
                         )
        #df = df.set_index(df.columns[0])
        #fig = df.iplot(asFigure=True, kind='scatter', mode='lines+markers', size=1)

	
    return fig



@app.callback(Output('output-data-upload', 'children'),
            [Input('process-data', 'n_clicks')],
                [State('upload-data', 'contents'),
                State('upload-data', 'filename')
            ])
def update_table(n_clicks,contents, filename):
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