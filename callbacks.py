from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import os
import dash_html_components as html
import dash_table
import pandas as pd
from app import app
import datetime as dt
from vas_functions import search_for_datafiles, scatter_graph, parse_data, params
from dash.exceptions import PreventUpdate

@app.callback([Output('datafiles_dropdown', 'options'),
               Output('datafiles_dropdown_memory','data')],
              [Input('datafiles_dropdown', 'value')])
def update_date_dropdown(value):
    if value == 'default':
        data_to_store = {}
    else:
        file = os.getcwd()+'\\input_data\\' + value
        df = pd.read_json(file)
        df=df.sort_index()
        data_to_store = df.to_dict('records')
    return [{'label': i, 'value': i} for i in search_for_datafiles()], data_to_store

@app.callback(Output('store_selected_files', 'data'),
            [Input('upload_selected_files', 'contents'),Input('upload_selected_files', 'filename')],
            [State('store_selected_files', 'data')]
              )
def import_data(contents, filename, existing_data):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        new_dataset = df.to_dict()
        #print(df)
    else:
        raise PreventUpdate()
    existing_data[str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]= new_dataset
    #print(existing_data)
    return existing_data

@app.callback(Output('uploaded_files_dropdown', 'options'),
             [Input('store_selected_files', 'data')]
              )
def update_file_dropdown(value):
    if value == 'default':
        raise PreventUpdate()
    else:
        option_list = list(value.keys())
    return [{'label': i, 'value': i} for i in option_list]

@app.callback(Output('uploaded_files_table', 'children'),
              [Input('uploaded_files_dropdown', 'value')],
              [State('store_selected_files', 'data')])
def show_selected_file(value,data):
    if value == 'default':
        raise PreventUpdate()
    else:
        table = html.Div([
            dash_table.DataTable(
                id='uploaded_files_table',
                data=data[value],
                columns=[{'name': str(i), 'id': str(i), "selectable": True} for i in range(len(data[value]))],
                editable=True,
                virtualization=True,
                column_selectable="multi",
                page_action="native",
                page_current=0,
                page_size=8
            ), ])
        #print(data[value])
        return table#html.H5(children='test', style={'textAlign': 'center'}),


@app.callback(Output('current_datafiles', 'children'),
            [Input('upload-data', 'contents'),Input('upload-data', 'filename')])
def import_data(contents, filename):
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
	   
@app.callback(Output('Mygraph', 'figure'),[Input('datafiles_dropdown', 'value')])
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

@app.callback([Output('visible_table', 'children'),
               Output('tag-options','options')],
              [Input('datafiles_dropdown', 'value'),
               Input('hidden_table','selected_columns')])
def update_table_and_dropdown(value,selected_columns):
    if value == 'default':
        return html.H5('no datafile selected'),[{"label": 'none', "value": 'none'}]
    else:
        file = os.getcwd()+'\\input_data\\' + value
        df = pd.read_json(file)
        df=df.sort_index()
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

@app.callback(Output('import-graph', 'figure'),
              [Input('datafiles_dropdown_memory', 'data'),
               Input('tag-options','value'),
               Input('hidden_table','selected_columns')])
def on_data_set_graph(raw_data,tags,selected):
    if raw_data == {}:
        return go.Figure()
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