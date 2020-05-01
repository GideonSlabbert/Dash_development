import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_table
#import dash_table_experiments as dt
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

countries = set(df['country'])

uploader_style = {'width': '100%',
                  'height': '35px',
                  'lineHeight': '35px',
                  'borderWidth': '1px',
                  'borderStyle': 'dashed',
                  'borderRadius': '5px',
                  'textAlign': 'center'
                  }

screening_graph_style = {'width': '99%',
               'borderRadius': '5px',
               'borderWidth': '1px',
               'height': '350px',
               'paper_bgcolor':'#FFFFFF',
               'plot_bgcolor':'#FFFFFF'
               }

import_graph_style = {'width': '100%',
               'borderRadius': '5px',
               'borderWidth': '1px',
               'borderColor': 'black',
               'height': '200px',
               'paper_bgcolor':'#FFFFFF',
               'plot_bgcolor':'#FFFFFF'     
               }

sel_link_style = {'color': 'white', 
                  'background':'black',
                  'borderWidth': '1px',
                  'borderStyle': 'solid',
                  'text-decoration': 'none'
                  }

unsel_link_style = {'color': 'black', 
                    'background':'#FFFFFF',
                    'borderWidth': '1px',
                    'borderStyle': 'solid',
                    'text-decoration': 'none'
                    }
#config = dict({'modeBarStyle': {
#        'orientation': 'h',
#        'backgroundColor': 'rgba(255 ,255 ,255 ,0.7)',
#        'iconColor': 'rgba(0, 31, 95, 0.3);'}
#    })


import_layout  = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Import Page', href='/apps/Import_Screen',style=sel_link_style),
    dcc.Link('Screening Graph', href='/apps/Screening_Graph',style=unsel_link_style),
    dcc.Link('Screening Table', href='/apps/Screening_Table',style=unsel_link_style),
    #dynamic elements:
    html.Div(children='''Step 1: Import data from excel/csv/textfile file'''),
    dcc.Upload(id='upload-data',children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
               style=uploader_style,multiple=True),     
  
    html.Div(id='current_datafiles')
])

graph_layout  = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Import Page', href='/apps/Import_Screen',style=unsel_link_style),
    dcc.Link('Screening Graph', href='/apps/Screening_Graph',style=sel_link_style),
    dcc.Link('Screening Table', href='/apps/Screening_Table',style=unsel_link_style),
    #dynamic elements:
    dcc.Graph(id='Mygraph',style=screening_graph_style)
])

table_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Import Page', href='/apps/Import_Screen',style=unsel_link_style),
    dcc.Link('Screening Graph', href='/apps/Screening_Graph',style=unsel_link_style),
    dcc.Link('Screening Table', href='/apps/Screening_Table',style=sel_link_style),
    #dynamic elements:
    html.Div([
    html.Div(id='imported-data-table'),#,style={'width': '70%', 'float':'left'}
        #html.Div(id='tag-options',style={'width': '29%', 'float':'left'}),
    html.Div(id='tag-selection'),
        dcc.Dropdown(
                    id='tag-options',
                    multi=True,
                    placeholder="Select tags to trend",
                    searchable=True
                    #style={'width': '29%', 'float':'right'}
                    )
            ]),
    html.Div(id='test'),
    dcc.Graph(id='import-graph',style=import_graph_style)
])