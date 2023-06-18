from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash_extensions.enrich import DashProxy
import dash_bootstrap_components as dbc

from Stock_Tracker_Dash import stocks_layout
from dona_diagnosis import dona_layout
from avas_place import game_layout

server = app.server

# Initialize dash app with proxy
app = DashProxy(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout for the main app
app.layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("AlphaBot", href="/stocktracker")),
            dbc.NavItem(dbc.NavLink("Dona's Diagnosis", href="/dona")),
            dbc.NavItem(dbc.NavLink("Ava's Place", href="/avasplace")),
        ],
        brand="Iddy's Playground",
        brand_href="/",
        sticky="top",
        dark=True,
        color="dark",
    ),
    dcc.Location(id='url', refresh=False),
    dbc.Container(id="page-content", fluid=True),
    dcc.Loading(id="loading-1", type="circle"),
], fluid=True)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dona':
        return dona_layout
    elif pathname == '/stocktracker':
        return stocks_layout
    elif pathname == '/avasplace':
        return game_layout
    else:
        return dbc.Jumbotron([
            dbc.Container([
                html.H1("Welcome to Iddy's Playground",
                        className="display-4"),
                html.P("This website showcases a variety of projects created by Idriss Animashaun. Each project is designed to be educational and engaging, with the goal of providing visitors with an opportunity to learn something new and have fun in the process. Whether you're interested in exploring new technologies, learning about cutting-edge research, or just looking for a bit of entertainment, Iddy's Playground has something for everyone. So come on in and start exploring!",
                        className='lead',
                        ),
            ], fluid=True)
        ])


if __name__ == '__main__':
    app.run_server(debug=False)
