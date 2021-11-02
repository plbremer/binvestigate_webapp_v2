from dash import html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import callback_context
import dash_daq as daq


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
                   # html.Button('bullshit button', id='bullshit button', n_clicks=0),
                   html.H3('Minimum Fold Change Magnitude')
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
                        dcc.Slider(
                            id='slider_additional',
                            min=0,
                            #max=max_fold_change,
                            max=50,
                            step=1,
                            value=0,
                            #marks={i:str(i)[0:5] for i in [i*(max_fold_change/20) for i in range(1,20)]}
                            marks={i:str(i) for i in range(51)}
                        )   
                    ]
                )
                #do not use width with sliders for some reason
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.H3('Don\'t Include Presence/Absence ----- Include Presence/Absence')
                    ]
                ),
                width='auto',
                #align='center'
            ),
            justify='center'
        ),
        #further slicing tools - include np.inf toggle
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        daq.ToggleSwitch(
                            id='toggleswitch_additional',
                            #label='include np.inf?',
                            value=True
                        )
                    ]
                )
            )
        )
    ]
)



@app.callback(
    [Output(component_id='slider_additional',component_property='value'),
    Output(component_id='toggleswitch_additional',component_property='value'),
    Output(component_id='store_additional',component_property='data')],
    
    [Input(component_id='slider_additional',component_property='value'),
    Input(component_id='toggleswitch_additional',component_property='value')],
    #Input(component_id='store_additional',component_property='modified_timestamp')],
    
    [State(component_id='store_additional',component_property='data')]
)
def callback_additional(
    slider_additional_value,
    toggleswitch_additional_value,
    #temp_modified_timestamp,
    store_additional_data
):
    #it was noticed that upon initial load, the  callback context had length >1
    #like
    #[{'prop_id': 'slider_additional.value', 'value': 0}, {'prop_id': 'toggleswitch_additional.value', 'value': True}]
    #this only works if the number of buttons is >1, but thats the case, so be it

    #therefore, we load from store if the callback context length is >1 and the store is not none
    print('-------------')
    print(callback_context.triggered)
    print(slider_additional_value)
    print(toggleswitch_additional_value)
    print(store_additional_data)

    if (len(callback_context.triggered)>1) and (store_additional_data is None):
        store_additional_data={
            'slider_additional':slider_additional_value,
            'toggleswitch_additional':toggleswitch_additional_value
        }
        return slider_additional_value,toggleswitch_additional_value,store_additional_data

    elif (len(callback_context.triggered)>1) and (store_additional_data is not None):
        slider_additional_value=store_additional_data['slider_additional']
        toggleswitch_additional_value=store_additional_data['toggleswitch_additional']
        return slider_additional_value,toggleswitch_additional_value,store_additional_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'slider_additional.value'):
        store_additional_data['slider_additional']=slider_additional_value
        return slider_additional_value,toggleswitch_additional_value,store_additional_data


    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id'] == 'toggleswitch_additional.value'):
        store_additional_data['toggleswitch_additional']=toggleswitch_additional_value
        return slider_additional_value,toggleswitch_additional_value,store_additional_data


    
