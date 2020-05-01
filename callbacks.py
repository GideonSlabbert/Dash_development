from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import os
import dash_html_components as html
import dash_table
import pandas as pd
from app import app
import datetime as dt
import dash_core_components as dcc
from vas_functions import search_for_datafiles, scatter_graph, parse_data
from dash.exceptions import PreventUpdate
import json

@app.callback([Output('datafiles-dropdown1', 'options'),
               Output('memory','data')],
              [Input('datafiles-dropdown1', 'value')])
def update_date_dropdown(value):
    if value == 'default':
        data_to_store = {}
    else:
        file = os.getcwd()+'\\input_data\\' + value
        df = pd.read_json(file)
        df=df.sort_index()
        data_to_store = df.to_dict('records')
    return [{'label': i, 'value': i} for i in search_for_datafiles()], data_to_store

@app.callback(Output('current_datafiles', 'children'),
            [Input('upload-data', 'contents'),Input('upload-data', 'filename')])
def import_data(contents, filename):
    list_of_files = []
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        filename_raw = os.path.splitext(filename)[0]
        filename_timestamp = filename_raw+'_'+dt.datetime.now().strftime("%Y_%m_%d_%H_%M")
        new_data_file = os.getcwd()+'\\input_data\\'+'{}.json'.format(filename_timestamp)
        df.to_json(new_data_file)
    list_of_files = search_for_datafiles()
    data = pd.DataFrame(list_of_files,columns =['File names'])
    table = html.Div([
                        dash_table.DataTable(
                            data=data.to_dict('rows'),
                            columns=[{'name': i, 'id': i} for i in data.columns])])
    return table
	   
@app.callback(Output('Mygraph', 'figure'),[Input('datafiles-dropdown1', 'value')])
def update_graph(value):
    if value == 'default':
        fig = go.Figure()
    else:
        file = os.getcwd()+'\\input_data\\' + value
        df = pd.read_json(file)
        df=df.sort_index()	
        df = df.set_index(df.columns[0])
        fig = scatter_graph(df)
    return fig

@app.callback([Output('imported-data-table', 'children'),
              Output('tag-options','options')],
              [Input('datafiles-dropdown1', 'value')])
def update_table_and_dropdown(value):
    if value == 'default':
        return html.H5('no datafile selected'),[{"label": 'none', "value": 'none'}]
    else:
        file = os.getcwd()+'\\input_data\\' + value
        df = pd.read_json(file)
        df=df.sort_index()
        table = html.Div([
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns],#, "selectable": True
                editable=True,
                virtualization=True,
                #column_selectable="multi",
                #selected_columns=[],
                page_action="native",
                page_current= 0,
                page_size= 5,
                ),])
        options=[{"label": i, "value": i} for i in df.columns.values.tolist()[1:]]
    return table, options

@app.callback(Output('import-graph', 'figure'),#Output()'test', 'children'
              [Input('memory', 'data'),
               Input('tag-options','value')])
def on_data_set_graph(raw_data,tags):
    if tags is None:
        return go.Figure()
        #return html.H5('no filtered tags')
    data = pd.DataFrame()
    data = data.from_dict(raw_data, orient='columns')
    data = data.sort_index()
    Date_index = data.columns.values.tolist().index('Date')
    df = data.set_index(data.columns[Date_index])
    fig = scatter_graph(df[tags])
    return fig
#    return dash_table.DataTable(
#            id='test-table',
#            data=data.to_dict('rows'),#[tags]
#            columns=[{'name': i, 'id': i} for i in data.columns.values.tolist()]#[tags]
#            #columns=[{'name': i, 'id': i} for i in list(filtered_data[0].keys())]
#        )

    

