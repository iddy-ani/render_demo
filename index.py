from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from Stock_Tracker_Dash import stocks_layout
import dash_bootstrap_components as dbc

# Import the layout and callback functions for Dona's Diagnosis
from dona_diagnosis import dona_layout
from avas_place import game_layout

server = app.server

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Iddy's Playground", className="display-6"),
        html.Hr(),
        html.P(
            "Explore The Pages Below", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("AlphaBot",
                            href="/stocktracker", active="exact"),
                dbc.NavLink("Dona's Diagnosis", href="/dona", active="exact"),
                dbc.NavLink("Ava's Place", href="/avasplace", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# Define the layout for the main app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    dcc.Loading(id="loading-1",
                children=[content],
                type="circle")
])

# Define the layout for the main app
home_layout = dbc.Container([
    dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Iddy's Playground", href='/'),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(
                            "Dona's Diagnosis", href="/dona")),
                        dbc.NavItem(dbc.NavLink(
                            "AlphaBot", href="/stocktracker")),
                    ],
                    className="ml-auto",
                    navbar=True
                )
            ]
        ),
        color="dark",
        dark=True,
        className="mb-5"
    ),
    dbc.Row([
        dbc.Col(
            html.H1("Welcome to Iddy's Playground",
                    className="text-center mb-5 mt-5"),
            width={"size": 12}
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.P("This website showcases a variety of projects created by Idriss Animashaun. Each project is designed to be educational and engaging, with the goal of providing visitors with an opportunity to learn something new and have fun in the process. Whether you're interested in exploring new technologies, learning about cutting-edge research, or just looking for a bit of entertainment, Iddy's Playground has something for everyone. So come on in and start exploring!",
                   className='lead',
                   ),
            width={"size": 12}
        )
    ])
], fluid=True)


# Define the callback for switching between pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dona':
        return dona_layout
    elif pathname == '/stocktracker':
        return stocks_layout
    elif pathname == '/avasplace':
        return game_layout
    elif pathname == '/':
        return home_layout


if __name__ == '__main__':
    app.run_server(debug=True)
