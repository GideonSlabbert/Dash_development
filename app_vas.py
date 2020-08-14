import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import datetime as dt
from styling import dropdown_style, uploader_style, screening_graph_style, import_graph_style, sel_link_style, unsel_link_style
import dash_table
from vas_functions import search_for_datafiles, scatter_graph, parse_data, params

external_stylesheets = ['https://codepen.io/chriddyp/pen/brPBPO.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H2(     children='Visual Analytic System',style={'textAlign':'center'}),
	html.H3(     children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Store(   id=      'datafiles_dropdown_memory'),
    dcc.Store(   id=      'store_selected_files',data={}),

    # dynamic elements:

    dcc.Upload(id='upload_selected_files', children=html.Div(['Drag and drop or ', html.A('"Click" to select files')]),style=uploader_style, multiple=True),

    html.Div('Dropdown displaying uploaded files:', style={'color': 'black', 'fontSize': 14}),
    dcc.Dropdown(id='uploaded_files_dropdown', options=[{'label': 'files', 'value': 'default'}], value='default'),#,'display': 'none'

    html.Div('Interactive table displaying selected files contents:', style={'color': 'black', 'fontSize': 14}),
    html.Div(dash_table.DataTable(id = 'hidden_view_table', data=[{}]), style={'display': 'none'}),
    html.Div(id='uploaded_files_table'),

    html.Div('Interactive graph displaying selected files contents:', style={'color': 'black', 'fontSize': 14}),
    dcc.Graph(id='import_graph',style=import_graph_style)
])

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
        df_table = pd.DataFrame.from_dict(data[value])
        df_table = df_table.sort_index()
        new_header = df_table.iloc[0]
        df_table = df_table[1:]
        df_table.columns = new_header
        if selected_columns is not None:
            list_of_sel_columns = selected_columns
        else:
            list_of_sel_columns = []

        table = html.Div([
            dash_table.DataTable(
                id='hidden_view_table',
                data=df_table.to_dict('rows'),
                columns=[*[{'name': 'Date', 'id':'Date', "selectable": False}]
                        ,*[{'name': i, 'id':i, "selectable": True} for i in df_table.columns[1:]]],
                editable=True,
                virtualization=True,
                column_selectable="multi",
                selected_columns=list_of_sel_columns,
                page_action="native",
                page_current=0,
                page_size=8
            ), ])

        #print(list_of_sel_columns)
        return table

# update graph component when a file is selected from the dropdown menu "uploaded_files_dropdown"
# The selected value is then used to filter the memory component "store_selected_files"
# a graph is automatically generated from the table (assump: time column is left column and first row is headings)
# The graph can then be changed to only display selected columns from the "hidden_view_table" element
@app.callback(Output('import_graph', 'figure'),
             [Input('uploaded_files_dropdown', 'value'), Input('hidden_view_table', 'selected_columns')],
             [State('store_selected_files', 'data')])
def on_data_set_graph(value,selected_columns,data):
    if value == 'default':
        raise PreventUpdate()
    else:
        df_table = pd.DataFrame.from_dict(data[value])      # read selected value from Store component and convert from dict to dataframe
        new_header = df_table.iloc[0]                       # assign first row as headers
        df_table = df_table[1:]                             # re-create dataframe without header row
        df_table.columns = new_header                       # assign dataframe columns with header values
        df_table = df_table.set_index(df_table.columns[0])  # set the first column as the index
        df_table = df_table.sort_index()                    # sort the dataframe according to the index (the dictionary scambles the rows)

    if selected_columns == [] or selected_columns is None:
        fig = scatter_graph(df_table)
    else:
        fig = scatter_graph(df_table[selected_columns])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)