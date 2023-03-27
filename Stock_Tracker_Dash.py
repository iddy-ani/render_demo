from app import app
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import yfinance as yf
import datetime as dt
import plotly.graph_objs as go
import datetime as dt
from dash.dependencies import Output, Input
import time


def get_stock_data(tickr):
    # stock = yf.Ticker(tickr).fast_info
    # print(stock)
    end = dt.datetime.now()
    start = end - dt.timedelta(days=7)
    stock_df = yf.download(tickr, start=start, end=end, interval='1m')
    return stock_df


tickr_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN',
              'META', 'INTC', 'CSCO', 'VZ', 'PFE', 'TSM']


df_list = [get_stock_data(tickr) for tickr in tickr_list]

colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'plot_colors': ['#FF5733', '#C70039', '#900C3F', '#581845', '#F39C12', '#D35400', '#2ECC71', '#1ABC9C', '#3498DB', '#9B59B6']
}


stocks_layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children="Iddy's Top Stock Tracker",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(
        children=['''
        A grid of Top Performing stocks
        ''',
                  html.Br(),
                  html.Br(),
                  '''
        Created by Idriss Animashaun
        ''',
                  html.Br(),
                  html.Br(),
                  '''
        Chart Updates Every 10m
        '''],
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(id='plots', children=[
        html.Div(
            [
                dcc.Graph(
                    id='stock-{}'.format(tickr),
                    figure={
                        'data': [
                            go.Candlestick(
                                x=df.index,
                                open=df['Open'],
                                high=df['High'],
                                low=df['Low'],
                                close=df['Close'],
                                increasing={'line': {'color': 'green'}},
                                decreasing={'line': {'color': 'red'}}
                            )
                        ],
                        'layout': {
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            },
                            'title': tickr,
                            'xaxis': {'title': 'Date'},
                            'yaxis': {'title': 'Price ($)'}
                        }
                    }
                )
                for df, tickr, color in zip(df_list, tickr_list, colors['plot_colors'])
            ],
            style={'columnCount': 2}
        )
    ]),
    dcc.Interval(
        id='interval-component',
        interval=10*60*1000,  # in milliseconds
        n_intervals=0
    )])


@app.callback(Output('plots', 'children'), [Input('interval-component', 'n_intervals')])
def update_plots(n):
    global df_list
    df_list = [get_stock_data(tickr) for tickr in tickr_list]
    return [
        dcc.Graph(
            id='stock-{}'.format(tickr),
            figure={
                'data': [
                    go.Candlestick(
                        x=df.index,
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name=tickr
                    )
                ],
                'layout': {
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    },
                    'title': tickr,
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Price ($)'}
                }
            }
        )
        for df, tickr, color in zip(df_list, tickr_list, colors['plot_colors'])
    ]
