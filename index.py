import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from layouts import graph_layout, table_layout, import_layout
import callbacks
dropdown_style = {"font-size": "small"}
from faultmap_search import faultmap_file_extraction

faultmap_data = faultmap_file_extraction("C:\FaultMap_data/faultmap_results_ss","/**/*csv*")
#faultmap_data_path = "C:\FaultMap_data/faultmap_results_ss"
#faultmap_files = glob.glob(faultmap_data_path + "/**/*csv*", recursive=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H5(children='Visual Analytic System',style={'textAlign':'center'}),
	html.H5(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Dropdown(id='datafiles-dropdown', options=[{'label': 'files', 'value': 'default'}],
                 value='default'),
    html.Div(id='page-content'),
    dcc.Dropdown(id='faultmap_files_main', options=[{'label': file, 'value': file} for file in faultmap_data.first_level_folder_options()],
                 value='default', style=dropdown_style),
    dcc.Dropdown(id='faultmap_files_sub', options=[{'label': 'files', 'value': 'default'}],
                 value='default'),
    dcc.Store(id='memory'),
    dcc.Store(id='faultmap_files',data=faultmap_data.main_file_list())
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])      
def display_page(pathname):
    if pathname == '/apps/Screening_Graph':
        return graph_layout
    elif pathname == '/apps/Screening_Table':
         return table_layout
    elif pathname == '/apps/Import_Screen':
         return import_layout
    else:
        return import_layout
        #return 'remember to add /apps/.. to http://127.0.0.1:8050 address'

if __name__ == '__main__':
    app.run_server(debug=True)