import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import graph_layout, table_layout, import_layout
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H5(children='Visual Analytic System',style={'textAlign':'center'}),
	html.H5(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),    
    dcc.Dropdown(id='datafiles-dropdown1',options=[{'label':'files', 'value':'master'}],
             value = 'default'),
    dcc.Store(id='memory'),
    html.Div(id='page-content')   
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