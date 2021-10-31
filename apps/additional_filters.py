
from dash import html
import dash_bootstrap_components as dbc

import pathlib

from app import app


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

layout=html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                #html.Div(
                children=[
                    html.Button('bullshit button', id='bullshit button', n_clicks=0),
                ],
                #),
                width='auto',
                align='center'
            )
        ),
    ]
)