from app import app
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import requests
import io


def get_stock_data():
    # URL of the file on Google Drive
    file_url = 'https://drive.google.com/file/d/1A283H_IBeXKQ9RHr8GiGq1CYTliHHIeL/view?usp=sharing'

    # Extract the file ID from the URL
    file_id = file_url.split('/')[-2]

    # Construct the new URL for downloading the file content
    download_url = f'https://drive.google.com/uc?id={file_id}'

    # Download the file content
    response = requests.get(download_url)
    content = response.content

    # Read the CSV content as a pandas DataFrame
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    return df


df_list = get_stock_data()


stocks_layout = html.Div(children=[
    html.H1(
        children="AlphaBot: The Ultimate Trading Bot for Top Performing Stocks",
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(
        children=['''
        Experience the Power of AI-Powered Trading
        '''],
        style={
            'textAlign': 'center'
        }
    ),
    html.Div(id='plots', children=[
        html.Div(
            [
                dcc.Graph(
                    id='stock-Equity',
                    figure={
                        'data': [
                            go.Scatter(
                                x=df_list['date'],
                                y=df_list['equity'],
                                name='Equity',
                                mode='lines'
                            )
                        ],
                        'layout': {
                            'title': 'Equity',
                            'xaxis': {'title': 'Date'},
                            'yaxis': {'title': 'Price ($)'}
                        }
                    }
                )
            ]
        )
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1*60*1000,  # in milliseconds
        n_intervals=0
    )])


@app.callback(Output('plots', 'children'), [Input('interval-component', 'n_intervals')])
def update_plots(n):
    global df_list
    df_list = get_stock_data()
    return [
        dcc.Graph(
            id='stock-Equity',
            figure={
                'data': [
                    go.Scatter(
                        x=df_list['date'],
                        y=df_list['equity'],
                        name='Equity',
                        mode='lines'
                    )
                ],
                'layout': {
                    'title': 'Equity',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Price ($)'}
                }
            }
        )
    ]
