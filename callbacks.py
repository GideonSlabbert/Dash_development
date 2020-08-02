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

# store contents of upload component (upload_selected_files) in store component (store_selected_files) by adding to what is already stored there
@app.callback(Output('store_selected_files', 'data'),
            [Input('upload_selected_files', 'contents'),Input('upload_selected_files', 'filename')],
            [State('store_selected_files', 'data')]
              )
def import_data(contents, filename, existing_data):
    if not contents:
        raise PreventUpdate
    else:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        new_dataset = df.to_dict()
    existing_data[filename+'_'+dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = new_dataset
    return existing_data

# populate dropdown component (uploaded_files_dropdown) from the store component (store_selected_files) dictionary keys
@app.callback(Output('uploaded_files_dropdown', 'options'),
             [Input('store_selected_files', 'data')]
              )
def update_file_dropdown(value):
    if value == 'default':
        raise PreventUpdate()
    else:
        option_list = list(value.keys())
    return [{'label': i, 'value': i} for i in option_list]

# update table component (uploaded_files_table) with other table component (hidden_view_table)
# when selecting a file from the dropdown component (uploaded_files_dropdown) with the data in the
# store component (store_selected_files) that matches the key from the dropdown list
# also captures the data from the selected columns of the hidden table
@app.callback(Output('uploaded_files_table', 'children'),
              [Input('uploaded_files_dropdown', 'value'),Input('hidden_view_table', 'selected_columns')],
              [State('store_selected_files', 'data')])
def show_selected_file(value,selected_columns,data):
    if value == 'default':
        raise PreventUpdate()
    else:
        list_of_sel_columns = []
        df_table = pd.DataFrame.from_dict(data[value])

        list_of_sel_columns = []
        if selected_columns is not None:
            list_of_sel_columns = selected_columns
        else:
            list_of_sel_columns = []

        table = html.Div([
            dash_table.DataTable(
                id='hidden_view_table',
                data=df_table.to_dict('rows'),
                columns=[{'name': str(i), 'id': str(i), "selectable": True} for i in df_table.columns],
                editable=True,
                virtualization=True,
                column_selectable="multi",
                selected_columns=list_of_sel_columns,
                page_action="native",
                page_current=0,
                page_size=8
            ), ])

        print(list_of_sel_columns)
        return table

#@app.callback(Output('import-graph', 'figure'),
#              [Input('datafiles_dropdown_memory', 'data'),
#               Input('tag-options','value'),
#               Input('hidden_table','selected_columns')])
#def on_data_set_graph(raw_data,tags,selected):
#    if raw_data == {}:
#        return go.Figure()
#    if selected is None:
#        return go.Figure()
#    else:
#        selected_columns = selected
#        data = pd.DataFrame()
#        data = data.from_dict(raw_data, orient='columns')
#        data = data.sort_index()
#        Date_index = data.columns.values.tolist().index('Date')
#        df = data.set_index(data.columns[Date_index])
#        fig = scatter_graph(df[selected_columns])
#    return fig