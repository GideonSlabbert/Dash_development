import dash_core_components as dcc
import dash_html_components as html

layout1  = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(children='Visual Analytic System',style={'textAlign':'center'}),
	html.H1(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Link('Go to 2.Screening_Table', href='/apps/2.Screening_Table'),
    html.Div(children='''Step 1: Import data from excel/csv/textfile file'''),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '35px',
            'lineHeight': '35px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
              },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Button(id='process-data',n_clicks = 0, children='Process the selected files',
                style={'width': '100%'}),     
    dcc.Graph(id='Mygraph',
              style={
                      'width': '100%',
                      'borderRadius': '5px',
                      'borderWidth': '1px',
                      'height': '350px',
                      'paper_bgcolor':'#FFFFFF',
                      'plot_bgcolor':'#FFFFFF'     
                      })
])

layout2 = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(children='Visual Analytic System',style={'textAlign':'center'}),
	html.H1(children='Fault Detection and Diagnosis',style={'textAlign':'center'}),
    dcc.Link('Go to 1.Screening_Graph', href='/apps/1.Screening_Graph'),
    html.Div(children='''Step 1: Import data from excel/csv/textfile file'''),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '35px',
            'lineHeight': '35px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
              },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Button(id='process-data',n_clicks = 0, children='Process the selected files',
                style={'width': '100%'}),
    html.Div(id='output-data-upload')
])