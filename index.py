import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from layouts import graph_layout, table_layout, import_layout
import callbacks
dropdown_style = {"font-size": "small"}
from faultmap_search import faultmap_file_extraction

faultmap_data = faultmap_file_extraction("C:\FaultMap_data/faultmap_results_ss","/**/*csv*")

uploader_style = {'width': '100%',
                  'height': '35px',
                  'lineHeight': '35px',
                  'borderWidth': '1px',
                  'borderStyle': 'dashed',
                  'borderRadius': '5px',
                  'textAlign': 'center'
                  }

app.layout = html.Div([
    dcc.Location(id=      'url', refresh=False),
    html.H5(     children='Visual Analytic System',style={'textAlign':'center'}),
	html.H5(     children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Dropdown(id=      'datafiles_dropdown', options=[{'label': 'files', 'value': 'default'}],value='default'),
    dcc.Upload(  id=      'upload_selected_files', children=html.Div(['Drag and drop or ', html.A('"Click" to select files')]),style=uploader_style, multiple=True),
    dcc.Store(   id=      'datafiles_dropdown_memory'),
    dcc.Store(   id=      'faultmap_files_memory',data=faultmap_data.main_file_list()),
    dcc.Store(   id=      'store_selected_files',data={}),
    html.Div(    id=      'page_content')
])

@app.callback(Output('page_content', 'children'),
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