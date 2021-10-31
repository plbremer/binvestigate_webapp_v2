#imports
#path stuff
#global variables/base dataset
#layout
#callbacks
import dash_table as dt
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import numpy as np
import pathlib
import pandas as pd

from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


my_dataframe=pd.read_pickle(DATA_PATH.joinpath('conglomerate_result_panda_count.bin'))
my_dataframe=my_dataframe.filter([
    'compound',
    'species_node_from',
    'disease_node_from',
    'organ_node_from',   
    'species_node_to',        
    'organ_node_to', 
    'disease_node_to',
    'fold_change', 
    'organ_node_from_path',
    'disease_node_from_path', 
    'organ_node_to_path', 
    'disease_node_to_path', 
    'included_triplets_from', 
    'included_triplets_to',
    'triplet_tuple_from', 
    'triplet_tuple_to',
    'possible_triplets_from', 
    'possible_triplets_to',
    'actual_triplets_from', 
    'ratio_from', 
    'actual_triplets_to', 
    'ratio_to',
    'min_count_from', 
    'min_count_to', 
    'sum_count_from', 
    'sum_count_to'
])

#gets something for the filter thingy
#max_fold_change=my_dataframe['fold_change'].astype(float,copy=True)[my_dataframe['fold_change'].astype(float,copy=True).abs() != np.inf].max()


#print(my_dataframe)

layout=html.Div(
    children=[
        #Table title
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.H1('Backend Dataset')
                    ]
                ),
                width='auto',
            ),
            justify='center'
        ),
        #resulting table
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        dt.DataTable(
                            id='subsetted_table',
                            columns=[{'name': temp, 'id': temp} for temp in my_dataframe.columns],
                            data=[]
                        )
                    ]
                ),
                width='auto'
            )
        ),






        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        #a header
                        html.Button(
                            'Click button to slice/filter dataset',
                            id='button_perform_slice',
                            n_clicks=0
                        )
                    ]
                ),
                width='auto'
            )
        )




















    ]
)





'''

@app.callback(
    [Output(component_id='subsetted_table',component_property='data')],
    [Input(component_id='store_cyto_compound',component_property='data')]#,
    # Input(component_id='cytoscape_species_from',component_property='selectedNodeData'),
    # Input(component_id='cytoscape_organ_from',component_property='selectedNodeData'),
    # Input(component_id='cytoscape_disease_from',component_property='selectedNodeData'),
    # Input(component_id='cytoscape_species_to',component_property='selectedNodeData'),
    # Input(component_id='cytoscape_organ_to',component_property='selectedNodeData'),
    # Input(component_id='cytoscape_disease_to',component_property='selectedNodeData'),
    # Input(component_id='slider_fold_change_numerical',component_property='value'),
    # Input(component_id='slice_results_checklist',component_property='value')]
    #[Input(component_id='button_perform_slice',component_property='n_clicks')],
    #[State(component_id='cytoscape_compound',component_property='elements'),

    # State(component_id='cytoscape_species_from',component_property='elements'),
    # State(component_id='cytoscape_organ_from',component_property='elements'),
    # State(component_id='cytoscape_disease_from',component_property='elements'),

    # State(component_id='cytoscape_species_to',component_property='elements'),
    # State(component_id='cytoscape_organ_to',component_property='elements'),
    # State(component_id='cytoscape_disease_to',component_property='elements'),

    #State(component_id='slider_fold_change_numerical',component_property='value'),
    #State(component_id='slice_results_checklist',component_property='value')]
)
def create_subsetted_graph_from_compound_nx(
    #we do nothing with temp_button_was_clicked
    # temp_button_was_clicked,
    # temp_compound_hierarchy,
    # temp_species_from_hierarchy,
    # temp_organ_from_hierarchy,
    # temp_disease_from_hierarchy,
    # temp_species_to_hierarchy,
    # temp_organ_to_hierarchy,
    # temp_disease_to_hierarchy,
    # temp_slider_value,
    # temp_include_inf_boolean
    temp_compound_store
):
    # selected_compound_list=return_nodes_selected(temp_compound_hierarchy,'compound')
    # selected_species_from_list=return_nodes_selected(temp_species_from_hierarchy,'species')
    # selected_organ_from_list=return_nodes_selected(temp_organ_from_hierarchy,'organ')
    # selected_disease_from_list=return_nodes_selected(temp_disease_from_hierarchy,'disease')
    # selected_species_to_list=return_nodes_selected(temp_species_to_hierarchy,'species')
    # selected_organ_to_list=return_nodes_selected(temp_organ_to_hierarchy,'organ')
    # selected_disease_to_list=return_nodes_selected(temp_disease_to_hierarchy,'disease')

    # print(selected_species_from_list)
    # print(selected_organ_from_list)
    # print(selected_disease_from_list)
    #hold=input('hold')
    #try:
    subsetted_dataframe=my_dataframe.loc[
        (my_dataframe['compound'].isin(temp_compound_store)) #&
            # (my_dataframe['species_node_from'].isin(selected_species_from_list)) &
            # (my_dataframe['organ_node_from'].isin(selected_organ_from_list)) &
            # (my_dataframe['disease_node_from'].isin(selected_disease_from_list)) &
            # (my_dataframe['species_node_to'].isin(selected_species_to_list)) &
            # (my_dataframe['organ_node_to'].isin(selected_organ_to_list)) &
            # (my_dataframe['disease_node_to'].isin(selected_disease_to_list))

            # (my_dataframe['species_node_from'].isin([temp_species_from_dict['id'] for temp_species_from_dict in temp_species_from_dict_list])) &
            # (my_dataframe['organ_node_from'].isin([temp_organ_from['id'] for temp_organ_from in temp_organ_from_dict_list])) &
            # (my_dataframe['disease_node_from'].isin([temp_disease_from_dict['id'] for temp_disease_from_dict in temp_disease_from_dict_list])) &
            # (my_dataframe['species_node_to'].isin([temp_species_to_dict['id'] for temp_species_to_dict in temp_species_to_dict_list])) &
            # (my_dataframe['organ_node_to'].isin([temp_organ_to_dict['id'] for temp_organ_to_dict in temp_organ_to_dict_list])) &
            # (my_dataframe['disease_node_to'].isin([temp_disease_to_dict['id'] for temp_disease_to_dict in temp_disease_to_dict_list]))        
    ]
    #except TypeError:
    #    subsetted_dataframe=my_dataframe

    #subset with slider
    #subsetted_dataframe=subsetted_dataframe.loc[
    #        subsetted_dataframe['fold_change'].astype(float,copy=True).abs().ge(temp_slider_value)
    #    ]

    #subset with checkbox
    # if temp_include_inf_boolean==False:
    #     subsetted_dataframe=subsetted_dataframe.loc[
    #             (subsetted_dataframe['fold_change'].astype(float,copy=True).abs() != np.inf)
    #         ]        

    subsetted_dataframe=[subsetted_dataframe.to_dict(orient='records')]
    return subsetted_dataframe

@app.callback(
    [Output(component_id='subsetted_table',component_property='columns')],
    [Input(component_id='button_perform_slice',component_property='n_clicks')]
)
def hello(temp):
    print('hi')
'''