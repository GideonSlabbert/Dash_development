from dash.dependencies import Input, Output
import base64

import io
import plotly.graph_objs as go


import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd
from app import app

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