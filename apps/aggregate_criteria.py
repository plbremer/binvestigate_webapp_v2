# the purpose of this script is
# when a button is clicked
# -some set of of criteria are checked
# -if they are met
# -the entire collection of stores are collected
# -
from dash import html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import callback_context


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


        dbc.Row(
            dbc.Col(
                #html.Div(
                children=[
                   # html.Button('bullshit button', id='bullshit button', n_clicks=0),
                   html.H3('Display number of filter sets waiting')
                ],
                #),
                width='auto',
                align='center'
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id='spinners_aggregate',
                    children=[]
                )
                #do not use width with sliders for some reason
            )
        ),








        dbc.Row(
            dbc.Col(
                #html.Div(
                children=[
                   # html.Button('bullshit button', id='bullshit button', n_clicks=0),
                   html.H3('All-search filters')
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
                        dcc.RangeSlider(
                            id='slider_aggregate',
                            min=0,
                            #max=max_fold_change,
                            max=10,
                            step=1,
                            #value=0,
                            #marks={i:str(i)[0:5] for i in [i*(max_fold_change/20) for i in range(1,20)]}
                            marks={i:str(i) for i in range(11)}
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






def check_for_errors(a,b):
    print('hi')







@app.callback(
    [#Output(component_id='store_compound',component_property='data'),
    #Output(component_id='store_additional',component_property='data'),
    Output(component_id='store_aggregate',component_property='data'),
    Output(component_id='slider_aggregate',component_property='value'),
    Output(component_id='spinners_aggregate',component_property='children')],
    
    [Input(component_id='button_aggregate',component_property='n_clicks'),
    Input(component_id='slider_aggregate',component_property='value')],
   
    
    [State(component_id='store_compound',component_property='data'),
    State(component_id='store_additional',component_property='data'),
    State(component_id='store_aggregate',component_property='data'),
    State(component_id='spinners_aggregate',component_property='children')]
)
def callback_compound(
    button_aggregate_n_clicks,
    slider_aggregate_value,


    store_compound_data,
    #temp_modified_timestamp,
    store_additional_data,
    store_aggregate_data,
    spinners_aggregate_children

):
    #it was noticed that upon initial load, the  callback context had length >1
    #like
    #[{'prop_id': 'slider_additional.value', 'value': 0}, {'prop_id': 'toggleswitch_additional.value', 'value': True}]
    #this only works if the number of buttons is >1, but thats the case, so be it

    #therefore, we load from store if the callback context length is >1 and the store is not none

    print('@@@@@@@@@@@@@@@@@@@@')
    print(callback_context.triggered)
    print(button_aggregate_n_clicks)
    print(slider_aggregate_value)
    print(store_compound_data)
    print(store_additional_data)
    print(store_aggregate_data)

    check_for_errors(store_compound_data,store_additional_data)

    #cases
    #on this page for first time and button is clicked and no errors




    #because we are beyond check for errors, we assume no error
    if (len(callback_context.triggered)>1) and (store_aggregate_data is None):
    # and (button_aggregate_n_clicks==0):

        store_aggregate_data={
            'compounds':[],
            'additional_slider':[],
            'additional_toggleswitch':[],
            'aggregate_on_page_rangeslider':None,
            'aggregate_on_page_spinners':0
        }



        #store_compound_data=None
        #store_additional_data=None
        return store_aggregate_data, slider_aggregate_value,spinners_aggregate_children

    elif (len(callback_context.triggered)>1) and (store_aggregate_data is not None):
        
        #restore the "post aggregate stuff" otherwise do nothing?
        slider_aggregate_value=store_aggregate_data['aggregate_on_page_rangeslider']


        #if store_aggregate_data['aggregate_on_page_spinners'] >0:
        for i in range(store_aggregate_data['aggregate_on_page_spinners']):
            spinners_aggregate_children.append(
                dbc.Spinner(
                    color='primary',
                    type='grow'
                )
            )            

        return store_aggregate_data, slider_aggregate_value,spinners_aggregate_children



    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='slider_aggregate.value'):
        
        store_aggregate_data['aggregate_on_page_rangeslider']=slider_aggregate_value
        return store_aggregate_data, slider_aggregate_value,spinners_aggregate_children

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_aggregate.n_clicks'):
        
        
        store_aggregate_data['compounds'].append(store_compound_data['compounds'])
        store_aggregate_data['additional_slider'].append(store_additional_data['slider_additional'])
        store_aggregate_data['additional_toggleswitch'].append(store_additional_data['toggleswitch_additional'])
        store_aggregate_data['aggregate_on_page_spinners']+=1

        spinners_aggregate_children.append(
            dbc.Spinner(
                color='primary',
                type='grow'
            )
        )

        #store_aggregate_data['aggregate_on_page_rangeslider']=slider_aggregate_value
        return store_aggregate_data, slider_aggregate_value,spinners_aggregate_children

    #return [store_aggregate_data]