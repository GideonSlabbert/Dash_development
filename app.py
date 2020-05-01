import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

# Loading screen CSS
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})
#.dash-loading CSS selector to apply specific styling while the table is waiting