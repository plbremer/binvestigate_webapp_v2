# the purpose of this script is
# when a button is clicked
# -some set of of criteria are checked
# -if they are met
# -the entire collection of stores are collected
# -




PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()



layout=html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                #html.Div(
                children=[
                   # html.Button('bullshit button', id='bullshit button', n_clicks=0),
                   html.H3('Collect all specified criteria')
                ],
                #),
                width='auto',
                align='center'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.Button(
                            'Aggregate all selections into one filter',
                            id='button_aggregate',
                            n_clicks=0
                        )
                    ]
                )
                #do not use width with sliders for some reason
            )
        ),
        # dbc.Row(
        #     dbc.Col(
        #         html.Div(
        #             children=[
        #                 #a header
        #                 html.H3('Don\'t Include Presence/Absence ----- Include Presence/Absence')
        #             ]
        #         ),
        #         width='auto',
        #         #align='center'
        #     ),
        #     justify='center'
        # ),
        # #further slicing tools - include np.inf toggle
        # dbc.Row(
        #     dbc.Col(
        #         html.Div(
        #             children=[
        #                 #a header
        #                 daq.ToggleSwitch(
        #                     id='toggleswitch_additional',
        #                     #label='include np.inf?',
        #                     value=True
        #                 )
        #             ]
        #         )
        #     )
        # )
    ]
)