import dash_core_components as dcc
import dash_html_components as html
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
    html.H5(     children='Visual Analytic System',style={'textAlign':'center'}),
	html.H5(     children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Store(   id=      'datafiles_dropdown_memory'),
    dcc.Store(   id=      'store_selected_files',data={}),
    # dynamic elements:
    # html.Button('Import Page', id='import_page',style=unsel_link_style),
    # html.Button('Screening Graph', id='screening_graph_page',style=unsel_link_style),
    # html.Button('Screening Table', id='screening_table_page',style=unsel_link_style),

    dcc.Upload(id='upload_selected_files', children=html.Div(['Drag and drop or ', html.A('"Click" to select files')]),
               style=uploader_style, multiple=True),
    html.Div('Dropdown displaying uploaded files:', style={'color': 'black', 'fontSize': 14}),
    dcc.Dropdown(id='uploaded_files_dropdown', options=[{'label': 'files', 'value': 'default'}], value='default'),
    html.Div(dash_table.DataTable(id = 'hidden_view_table', data=[{}]), style={'display': 'none'}),
    html.Div(id='uploaded_files_table'),
    html.Div(id = 'view_table'),
    html.Div(id='data'),
    dcc.Graph(id='Mygraph',style=screening_graph_style),
    html.Div(    id=      'page_content')
])

# populate dropdown component (uploaded_files_dropdown) from the store component (store_selected_files) dictionary keys
# @app.callback([Output('import_page', 'style'),Output('screening_graph_page', 'style'),Output('screening_table_page', 'style')],
#               [Input('import_page', 'n_clicks_timestamp'),Input('screening_graph_page', 'n_clicks_timestamp'),Input('screening_table_page', 'n_clicks_timestamp')]
#               )
# def change_to_import_page(import_click,screening_graph_click,screening_table_click):
#     if import_click is None and screening_graph_click is None and screening_table_click is None:
#         raise PreventUpdate()
#     if import_click is None:
#         import_click = 1
#     if screening_graph_click is None:
#         screening_graph_click = 1
#     if screening_table_click is None:
#         screening_table_click = 1
#     if int(import_click) > int(screening_graph_click) and int(import_click) > int(screening_table_click):
#         return sel_link_style,unsel_link_style,unsel_link_style
#     if int(screening_graph_click) > int(import_click) and int(screening_graph_click) > int(screening_table_click):
#         return unsel_link_style,sel_link_style,unsel_link_style
#     if int(screening_table_click) > int(import_click) and int(screening_table_click) > int(screening_graph_click):
#         return unsel_link_style,unsel_link_style,sel_link_style

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
                column_selectable="single",
                selected_columns=list_of_sel_columns,
                page_action="native",
                page_current=0,
                page_size=8
            ), ])

        print(list_of_sel_columns)
        return table

if __name__ == '__main__':
    app.run_server(debug=True)