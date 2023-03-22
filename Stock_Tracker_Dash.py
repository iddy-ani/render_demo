# Yes, here is an example of how to create a Dash web page with a grid of stock values using Plotly.

import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import yfinance as yf
import datetime as dt

app = dash.Dash()
server = app.server


def get_stock_data(tickr):
    # stock = yf.Ticker(tickr).fast_info
    # print(stock)
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365)
    stock_df = yf.download(tickr, start=start, end=end)
    return stock_df


tickr_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN',
              'FB', 'INTC', 'CSCO', 'VZ', 'PFE', 'TSM']


df_list = [get_stock_data(tickr) for tickr in tickr_list]

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Stock Visualization',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(
        children='''
        A grid of 10 stock values.
        ''',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(
        [
            dcc.Graph(
                id='stock-{}'.format(tickr),
                figure={
                    'data': [
                        {'x': df['Close'].index, 'y': df['Close'].values,
                            'type': 'line', 'name': tickr}
                        for df, tickr in zip(df_list, tickr_list)
                    ],
                    'layout': {
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        }
                    }
                }
            ) for df, tickr in zip(df_list, tickr_list)
        ],
        style={'columnCount': 2}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

# # This code will create a Dash web page that has a grid of 10 line plots, with one plot for each stock value in the tickr_list. You can adjust the number of columns in the grid by changing the columnCount property in the style dictionary. The get_stock_data function downloads the historical stock data using yfinance, and the Plotly Express library is used to create the line plots.
