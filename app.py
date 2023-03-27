import dash
import dash_bootstrap_components as dbc

# Set up the main app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
