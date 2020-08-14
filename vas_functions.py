import os
import plotly.graph_objs as go
import base64
import io
import pandas as pd
import dash_html_components as html
import numpy as np

#template = "plotly"
#template = "plotly_white"
#template = "ggplot2"
#template = "plotly_dark"
#template = "seaborn"
template = "simple_white"
#template = "none"


def search_for_datafiles():
    path = os.getcwd()+'\\input_data'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                #files.append(os.path.join(r, file))
                files.append(file)
    
    return files
                
def scatter_graph(df):
    fig = go.Figure()
    y_index = 1
    for value in df.iteritems():
        fig.add_trace(
                go.Scattergl(x = df.index,
							 y = value[1],
                             name = value[0],
                             yaxis = 'y'+str(y_index),
                             line_shape='hv'#,
                             #mode='lines+markers'
							)
                      )
        fig['layout'].update({'yaxis{}'.format(y_index):dict(visible=False,autorange=True)}
                             #,xaxis=dict(rangeslider=dict(visible=True))#,type='date'
                            )
        
        y_index += 1
        
    fig.update_layout(xaxis_showgrid=False, 
                      yaxis_showgrid=False,
                      showlegend=True,
                      margin=dict(l=10, r=10, t=10, b=20)
                      #,paper_bgcolor="#FFFFFF"
                      #,plot_bgcolor="#FFFFFF"
                      ,template=template
                      ,modebar=dict(orientation='v',bgcolor='rgba(0,0,0,0.1)')

                      )
    
    fig.update_traces(
                        line=dict(width=1.5),
                        #marker=dict(opacity=1)
                     )	

    return fig

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=None)
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+', header=None)
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])
    return df

def params(df):
    columns = ['param'] + df.keys().to_list()[2:]
    max_list = ['Max']
    min_list = ['Min']
    median_list = ['Median']
    mean_list = ['Mean']
    std_list = ['StdDev']
    nans = ['Nans']
    for index_label in df.keys().to_list()[2:]:
        max_list.append(
                        np.round(np.nanmax(df['{}'.format(index_label)].to_list()),1)
                       )
        min_list.append(
                    np.round(np.nanmin(df['{}'.format(index_label)].to_list()),1)
                   )
        median_list.append(
                    np.round(np.nanmedian(df['{}'.format(index_label)].to_list()),1)
                   )
        mean_list.append(
                    np.round(np.nanmean(df['{}'.format(index_label)].to_list()),1)
                   )
        std_list.append(
                    np.round(np.nanstd(df['{}'.format(index_label)].to_list()),1)
                   )
        nans.append(np.any(np.isnan(df['{}'.format(index_label)].to_list())))
                
    max_list = [(max_list),(min_list),(median_list),(mean_list),(std_list),(nans)]
    df = pd.DataFrame.from_records(max_list, columns=columns)
    return df
    