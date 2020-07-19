import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app
from layouts import graph_layout, table_layout, import_layout
import callbacks
dropdown_style = {"font-size": "small"}
import glob
faultmap_data_path = "C:\FaultMap_data/faultmap_results_ss"
faultmap_files = glob.glob(faultmap_data_path + "/**/*csv*", recursive=True)

#use .replace to remove path from file names
faultmap_files_cleaned = [file.replace(faultmap_data_path, '') for file in faultmap_files]

#use .partition to extract a list of all the first folder names
#                           first partition using "\\" target
#                                          specify which element in the partition to extract - 2nd element is the string after the target "\\"
#                                              do a second partition with the target "\\" and this time extract the elemtn before the target
faultmap_files_main = [
                        [file.partition("\\")[2].partition("\\")[0] for file in faultmap_files_cleaned],
                        [file for file in faultmap_files_cleaned]
                        ]
# use set() to filter out unique entries an convert back to a list
faultmap_files_main = list(set(faultmap_files_main[0]))

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H5(children='Visual Analytic System',style={'textAlign':'center'}),
	html.H5(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Dropdown(id='faultmap_files_main', options=[{'label': file, 'value': file} for file in faultmap_files_main],
                 value='default',style=dropdown_style),
    dcc.Dropdown(id='faultmap_files_sub', options=[{'label': 'files', 'value': 'default'}],
                 value='default'),
    dcc.Dropdown(id='datafiles-dropdown', options=[{'label': 'files', 'value': 'default'}],
                 value='default'),
    html.Div(id='page-content'),
    dcc.Store(id='memory'),
    dcc.Store(id='faultmap_files')
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