from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import os
import dash_html_components as html
import dash_table
import pandas as pd
from app import app
import datetime as dt
import dash_core_components as dcc
from vas_functions import search_for_datafiles, scatter_graph, parse_data, params
from dash.exceptions import PreventUpdate
import json

@app.callback(Output('faultmap_files_sub', 'options'),
              [Input('faultmap_files_main', 'value'),Input('faultmap_files','data')])
def update_faultmap_files_dropdown(value,faultmap_data_files):
    if value == 'default':
        raise PreventUpdate
        filtered_files = ['no file selected']
    else:
        filtered_files = [file for index,file in enumerate(faultmap_data_files[1]) if faultmap_data_files[0][index] == value]
        if len(filtered_files) == 0:
            filtered_files = ['no entries found']
    return [{'label': file, 'value': file} for file in filtered_files]#, data_to_store

@app.callback(Output('faultmap_files_sub', 'value'),
              [Input('faultmap_files_sub', 'options')])
def set_value(value):
    return value[0]['value']

@app.callback([Output('datafiles-dropdown', 'options'),
               Output('memory','data')],
              [Input('datafiles-dropdown', 'value')])
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
	   
@app.callback(Output('Mygraph', 'figure'),[Input('datafiles-dropdown', 'value')])
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

#@app.callback(Output('visible_table', 'children'),
#              [Input('memory', 'data'),
#               Input('hidden_table','selected_columns')])
#def test(memory,cells):
#    if memory is None:
#        #memory = {}
#        raise PreventUpdate
#        table = html.Div(['no data yet'])
#    else:
#        data = pd.DataFrame()
#        data = data.from_dict(memory, orient='columns')
#        #data = data.sort_index()
##        print(cells)
#        list_of_sel_columns = []
#        if cells is not None:
#            list_of_sel_columns = cells
#        else:
#            list_of_sel_columns = []
##        if cells is not None:
##            for item in cells:
##                list_of_sel_columns.append(data.columns.values.tolist().index(item))
#            
#        columns = data.keys().to_list()
#        table = html.Div([
#                dash_table.DataTable(
#                    id='hidden_table',
#                    data=data.to_dict('rows'),
#                    columns=[{'name': i, 'id': i, "selectable": True} for i in columns],#
#                    editable=True,
#                    virtualization=True,
#                    column_selectable="multi",
#                    selected_columns=list_of_sel_columns,
#                    page_action="native",
#                    page_current= 0,
#                    page_size= 5,
#                    ),])
#    return table
    

@app.callback([Output('visible_table', 'children'),
               Output('tag-options','options')],
              [Input('datafiles-dropdown', 'value'),
               Input('hidden_table','selected_columns')])
def update_table_and_dropdown(value,selected_columns):
    if value == 'default':
        return html.H5('no datafile selected'),[{"label": 'none', "value": 'none'}]
    else:
        file = os.getcwd()+'\\input_data\\' + value
        df = pd.read_json(file)
        df=df.sort_index()
#        print(selected_columns)
        list_of_sel_columns = []
        if selected_columns is not None:
            list_of_sel_columns = selected_columns
        else:
            list_of_sel_columns = []
        
        Date_index = df.columns.values.tolist().index('Date')
        df = df.set_index(df.columns[Date_index])        
        descriptive_data = params(df)
        table = html.Div([
            dash_table.DataTable(
                id='hidden_table',
                data=descriptive_data.to_dict('rows'),
                columns=[{'name': i, 'id': i, "selectable": True} for i in descriptive_data.columns],#
                editable=True,
                virtualization=True,
                column_selectable="multi",
                selected_columns=list_of_sel_columns,
                page_action="native",
                page_current= 0,
                page_size= 8
                ),])
        
        options=[{"label": i, "value": i} for i in df.columns.values.tolist()[1:]]
    return table, options

@app.callback(Output('import-graph', 'figure'),#Output()'test', 'children'
              [Input('memory', 'data'),
               Input('tag-options','value'),
               Input('hidden_table','selected_columns')])
def on_data_set_graph(raw_data,tags,selected):
#    if tags is None:
#        print(selected)
#        return go.Figure()
    if raw_data == {}:
        return go.Figure()

        
        #return html.H5('no filtered tags')
#    print(selected)

    if selected is None:
        return go.Figure()
    else:
        selected_columns = selected
        data = pd.DataFrame()
        data = data.from_dict(raw_data, orient='columns')
        data = data.sort_index()
        Date_index = data.columns.values.tolist().index('Date')
        df = data.set_index(data.columns[Date_index])
        fig = scatter_graph(df[selected_columns])
    return fig
#    return dash_table.DataTable(
#            id='test-table',
#            data=data.to_dict('rows'),#[tags]
#            columns=[{'name': i, 'id': i} for i in data.columns.values.tolist()]#[tags]
#            #columns=[{'name': i, 'id': i} for i in list(filtered_data[0].keys())]
#        )

    

