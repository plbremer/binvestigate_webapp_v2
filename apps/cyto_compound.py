
import dash_bootstrap_components as dbc
from dash import html
import dash_cytoscape as cyto
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
from dash import callback_context
import dash_core_components as dcc

from itertools import chain
import networkx as nx
import pathlib
import json
from pprint import pprint
import fnmatch

from app import app

cyto.load_extra_layouts()

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


#load the base compound network
compound_json_address=DATA_PATH.joinpath('cyto_format_compound.json')
temp_json_file=open(compound_json_address,'r')
compound_network_dict=json.load(temp_json_file)
temp_json_file.close()
for temp_element in compound_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    try:
        temp_element['data']['label']='Bin: '+temp_element['data']['common_name']
    except KeyError:
        temp_element['data']['label']=temp_element['data']['name']
    
    temp_element['classes']='not_selected'


# options=[
#     {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in compound_network_dict['elements']['nodes']
# ]

# print(options)
# hold=input('hold')


#defines the map between the various boxes and the node ids
checklist_hashmap={
    'both_glucoses': ['5','22'],
    'alanine':['2']
}


basic_stylesheet=[
    {
        'selector':'node',
        'style':{
            'content':'data(label)',
            'text-wrap':'wrap',
            'text-max-width':100,
            'font-size':13
        }
        
    },
    # {
    #     'selector':'.selected',
    #     'style':{
    #         'background-color':'red'
    #     }
    # }
    #'text-wrap':'wrap'
    {
        'selector':'.selected',
        'style':{
            'background-color':'red'
        }
    },
    {
        'selector':'.not_selected',
        'style':{
            'background-color':'grey'
        }
    }
]

networkx_address=DATA_PATH.joinpath('compounds_networkx.bin')
networkx=nx.readwrite.gpickle.read_gpickle(networkx_address)


layout=html.Div(
    children=[
        # dbc.Row(
        #     dbc.Col(
        #         children=[
        #             html.Button('add compound cyto', id='button_add_cyto_compound', n_clicks=0),
        #         ],
        #         width='auto',
        #         align='center'
        #     )
        # ),
        html.Div(
            id='div_cytoscape_compound_cyto',
            children=[
                cyto.Cytoscape(
                    id='cytoscape_compound',
                    layout={'name':'dagre'},
                    elements=compound_network_dict['elements'],
                    minZoom=0.3,
                    maxZoom=5,
                    stylesheet=basic_stylesheet
                )
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            dcc.Checklist(
                                id='checklist_compound',
                                options=[
                                    {'label': 'both glucoses', 'value': 'both_glucoses'},
                                    {'label': 'alanine', 'value': 'alanine'}
                                ]
                            )
                        ],
                        width='auto',
                        align='center'
                    )
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            dcc.Dropdown(
                                id='dropdown_compound',
                                options=[
                                    {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in compound_network_dict['elements']['nodes']
                                ],
                                multi=True
                            )
                        ],
                        #width='auto',
                        #align='center'
                    )
                ),
            ]
        ),
        html.Div(    
            children=[
                dbc.Row(
                    dbc.Col(
                        children=[
                            html.Button(
                                'Reset selections',
                                id='Button_compound',
                            )
                        ],
                        #width='auto',
                        #align='center'
                    )
                ),
            ]
        ),

    
    ]
)


@app.callback(
    [Output(component_id='cytoscape_compound',component_property='elements'),
    Output(component_id='checklist_compound',component_property='value'),
    Output(component_id='dropdown_compound',component_property='value'),
    Output(component_id='store_compound',component_property='data')],
    
    [Input(component_id='cytoscape_compound',component_property='tapNodeData'),
    Input(component_id='checklist_compound',component_property='value'),
    Input(component_id='dropdown_compound',component_property='value')],#,
    #Input(component_id='store_compound',component_property='modified_timestamp')],
    
    [State(component_id='cytoscape_compound',component_property='elements'),
    State(component_id='store_compound',component_property='data')]
)
def callback_aggregate(
    cytoscape_compound_tapnodedata,
    checklist_compound_value,
    dropdown_compound_value,
    #store_compound_modified_timestamp,
    cytoscape_compound_elements,
    store_compound_data
):
    print('@')
    print(callback_context.triggered)


    if (callback_context.triggered[0]['prop_id'] == 'cytoscape_compound.tapNodeData') and (callback_context.triggered[0]['value'] is not None):

        try:
            child_nodes_and_self=nx.algorithms.dag.descendants(networkx,cytoscape_compound_tapnodedata['id'])
        except nx.NetworkXError:
            child_nodes_and_self=set()
        
        child_nodes_and_self.add(cytoscape_compound_tapnodedata['id'])
        child_nodes_and_self=set(map(str,child_nodes_and_self))

        #for temp_id in child_nodes_and_self:
            #update elements
        #    if 

            #update store

            #update dropdown

        #update elements
        for temp_node in cytoscape_compound_elements['nodes']:
        #    print(temp_node['data'])    
            if temp_node['data']['id'] in child_nodes_and_self:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'        

        #update store
        #store should be exactly the same thing as chosen elements
        #cant just add the chosen ones because repeated selections can lead to unusual combos
        temp_store={
            'compounds':[],
            'checkboxes':[]
        }
        for temp_node in cytoscape_compound_elements['nodes']:
            if temp_node['classes']=='selected':
                temp_store['compounds'].append(temp_node['data']['id'])
        
        #update multi
        temp_dropdown_values=temp_store['compounds']

        #update checkbox
        checkbox_values=[]
        #if (('22' in temp_store) and ('5' in temp_store)):
        # #   checkbox_values.append('both_glucoses')
        for temp_checkbox in checklist_hashmap.keys():
            print(temp_checkbox)
            #if every node id is in the store
            #print([(i in temp_store['compounds']) for i in checklist_hashmap[temp_checkbox]])
            if all([(i in temp_store['compounds']) for i in checklist_hashmap[temp_checkbox]]):
                checkbox_values.append(temp_checkbox)
                temp_store['checkboxes'].append(temp_checkbox)
        #hold=input('hold')

        print(checkbox_values)

        return cytoscape_compound_elements, checkbox_values, temp_dropdown_values,temp_store
        
        # print('---------------')
        # print(child_nodes_and_self)


    elif (callback_context.triggered[0]['prop_id'] == 'checklist_compound.value'):
        #elements
        #store
        #checklist
        #dropdown
        #print(callback_context.triggered)
        #print(checklist_compound_value)
        if (store_compound_data is None):
            print('we clicked, it was the first click')
            #hold=input('hold')
            box_we_clicked=checklist_compound_value[0]

            #elements
            #store
            #checklist
            #dropdown

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap[box_we_clicked]:
                    #if temp_node['classes']=='selected':
                    #    temp_node['classes']='not_selected'
                    #elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'  
            
            #store
            store_compound_data={
                'compounds':[],
                'checkboxes':[]
            }
            store_compound_data['checkboxes'].append(box_we_clicked)
            store_compound_data['compounds']=checklist_hashmap[box_we_clicked]

            #checklist
                #checklist_compound_value=checklist_compound_value+box_we_clicked
            #dropdown
            temp_dropdown_values=store_compound_data['compounds']

            return cytoscape_compound_elements, checklist_compound_value, temp_dropdown_values,store_compound_data

        elif len(store_compound_data['checkboxes']) > len(checklist_compound_value):
            print('we unclicked')
            box_we_unclicked=list(set(store_compound_data['checkboxes']).difference(set(checklist_compound_value)))[0]

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap[box_we_unclicked]:
                    #if temp_node['classes']=='selected':
                    #    temp_node['classes']='not_selected'
                    #elif temp_node['classes']=='not_selected':
                    temp_node['classes']='not_selected'         

            #store
            store_compound_data['checkboxes'].remove(box_we_unclicked)
            print(set(store_compound_data['compounds']))
            print(set(checklist_hashmap[box_we_unclicked]))
            print(set(store_compound_data['compounds']).difference(set(checklist_hashmap[box_we_unclicked])))
            store_compound_data['compounds']=list(set(store_compound_data['compounds']).difference(set(checklist_hashmap[box_we_unclicked])))

            #checklist
            #checklist_compound_value=checklist_compound_value+box_we_clicked
            #dropdown
            temp_dropdown_values=store_compound_data['compounds']            

            return cytoscape_compound_elements, checklist_compound_value, temp_dropdown_values,store_compound_data


        elif (len(store_compound_data['checkboxes']) < len(checklist_compound_value)):
            print('we clicked')
            #hold=input('hold')
            box_we_clicked=list(set(checklist_compound_value).difference(set(store_compound_data['checkboxes'])))[0]
            print(box_we_clicked)
            #elements
            #store
            #checklist
            #dropdown

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap[box_we_clicked]:
                    #if temp_node['classes']=='selected':
                    #    temp_node['classes']='not_selected'
                    #elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'  
            
            #store
            store_compound_data['checkboxes'].append(box_we_clicked)
            print(set(store_compound_data['compounds']))
            print(set(checklist_hashmap[box_we_clicked]))
            print(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))
            store_compound_data['compounds']=list(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))

            #checklist
            #checklist_compound_value=checklist_compound_value+box_we_clicked
            #dropdown
            temp_dropdown_values=store_compound_data['compounds']

            return cytoscape_compound_elements, checklist_compound_value, temp_dropdown_values,store_compound_data



        else:
            print('we shouldnt be here')

        # total_checked_list=list()
        # for temp_checkbox in checklist_hashmap.keys():
        #     #if one of the possible checkboxes has been checked
        #     if temp_checkbox in checklist_compound_value:
        #         #ensure that every corresponding node is clicked and such
        #         #to avoid nested for loops we make one complete list of all nodes that should be checked
        #         total_checked_list+=checklist_hashmap[temp_checkbox]
        # #then we go through the elements once
        # #setting them all to selected (this should be redundant/unnecessary for all but one set)
        # for temp_node in cytoscape_compound_elements['nodes']:
        #     if temp_node['data']['id'] in total_checked_list:
        #         #if temp_node['classes']=='selected':
        #         #    temp_node['classes']='not_selected'
        #         #elif temp_node['classes']=='not_selected':
        #         temp_node['classes']='selected'       
        
    elif (callback_context.triggered[0]['prop_id'] == 'dropdown_compound.value'):

        if (store_compound_data is None):
            print('hi')
            compound_we_added=dropdown_compound_value[0]
            print(compound_we_added)
            #elements
            #store
            #checklist
            #dropdown

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] == compound_we_added:
                    #if temp_node['classes']=='selected':
                    #    temp_node['classes']='not_selected'
                    #elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_compound_data={
                'compounds':[],
                'checkboxes':[]
            }            

            store_compound_data['compounds'].append(compound_we_added)
            #print(set(store_compound_data['compounds']))
            #print(set(checklist_hashmap[box_we_clicked]))
            #print(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))
            #store_compound_data['compounds'].append(compound_we_added)#=list(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))

            #checklist
            #checklist_compound_value=checklist_compound_value+box_we_clicked
            #so the general logic is
            #we chose a compound
            #that compound belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of compounds is selected (the currently chosen compound)
            #being the "completing compound"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_compound_belongs=list()
            checkboxes_to_which_this_compound_belongs=[temp_key for temp_key in checklist_hashmap.keys() if (compound_we_added in checklist_hashmap[temp_key])]
            checklist_compound_value=[]
            for temp_checkbox in checkboxes_to_which_this_compound_belongs:
                #if the set of compounds implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of compounds is there by doing a difference and if the difference length is zero
                
                if len(set(checklist_hashmap[temp_checkbox]).difference(set(dropdown_compound_value)))==0:
                    store_compound_data['checkboxes'].append(temp_checkbox)
                    checklist_compound_value.append(temp_checkbox)


            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data



















        elif len(store_compound_data['compounds']) > len(dropdown_compound_value):
            print('hi')
            #elements
            #store
            #checklist
            #dropdown

            print('we subtracted')
            #hold=input('hold')
            compound_we_lost=list(set(store_compound_data['compounds']).difference(set(dropdown_compound_value)))[0]
            print(compound_we_lost)
            #elements
            #store
            #checklist
            #dropdown

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] == compound_we_lost:
                    #if temp_node['classes']=='selected':
                    #    temp_node['classes']='not_selected'
                    #elif temp_node['classes']=='not_selected':
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_compound_data['compounds'].remove(compound_we_lost)
            #print(set(store_compound_data['compounds']))
            #print(set(checklist_hashmap[box_we_clicked]))
            #print(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))
            #store_compound_data['compounds'].append(compound_we_added)#=list(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))

            #checklist
            #checklist_compound_value=checklist_compound_value+box_we_clicked
            #so the general logic is
            #we chose a compound
            #that compound belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of compounds is selected (the currently chosen compound)
            #being the "completing compound"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_compound_belongs=list()
            checkboxes_to_which_this_compound_belongs=[temp_key for temp_key in checklist_hashmap.keys() if (compound_we_lost in checklist_hashmap[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_compound_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                
                #if len(set(checklist_hashmap[temp_checkbox]).difference(set(dropdown_compound_value)))==0:
                #
                try:
                    store_compound_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_compound_value.remove(temp_checkbox)
                except ValueError:
                    continue


            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data



        elif len(store_compound_data['compounds']) < len(dropdown_compound_value):
            print('hi')
            #elements
            print('we added')
            #hold=input('hold')
            compound_we_added=list(set(dropdown_compound_value).difference(set(store_compound_data['compounds'])))[0]
            print(compound_we_added)
            #elements
            #store
            #checklist
            #dropdown

            #elements
            for temp_node in cytoscape_compound_elements['nodes']:
                if temp_node['data']['id'] == compound_we_added:
                    #if temp_node['classes']=='selected':
                    #    temp_node['classes']='not_selected'
                    #elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_compound_data['compounds'].append(compound_we_added)
            #print(set(store_compound_data['compounds']))
            #print(set(checklist_hashmap[box_we_clicked]))
            #print(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))
            #store_compound_data['compounds'].append(compound_we_added)#=list(set(store_compound_data['compounds']).union(set(checklist_hashmap[box_we_clicked])))

            #checklist
            #checklist_compound_value=checklist_compound_value+box_we_clicked
            #so the general logic is
            #we chose a compound
            #that compound belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of compounds is selected (the currently chosen compound)
            #being the "completing compound"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_compound_belongs=list()
            checkboxes_to_which_this_compound_belongs=[temp_key for temp_key in checklist_hashmap.keys() if (compound_we_added in checklist_hashmap[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_compound_belongs:
                #if the set of compounds implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of compounds is there by doing a difference and if the difference length is zero
                
                if len(set(checklist_hashmap[temp_checkbox]).difference(set(dropdown_compound_value)))==0:
                    store_compound_data['checkboxes'].append(temp_checkbox)
                    checklist_compound_value.append(temp_checkbox)


            return cytoscape_compound_elements, checklist_compound_value, dropdown_compound_value,store_compound_data

        else:
            print('we shouldnt be here part 2')





        #elements
        #elements_implied_by_selection=checklist_hashmap[]
        #there are two things to do
        #1, make sure that every box that is checked is entirely "on/selected" in store/elements
        #2, if there is a checkbox that is entirely "on" within the store/elements, then that is the box that was unchecked, so remove the full set



        #return cytoscape_compound_elements, checkbox_values, temp_dropdown_values,store_compound_data

    elif (callback_context.triggered[0]['prop_id'] == 'cytoscape_compound.tapNodeData') and (callback_context.triggered[0]['value'] is None):
        print('-------------------------------------------------------------')
        
        pprint(cytoscape_compound_tapnodedata),
        pprint(checklist_compound_value),
        pprint(dropdown_compound_value),
        #pprint(store_compound_modified_timestamp),
        pprint(cytoscape_compound_elements),
        pprint(store_compound_data)

        for temp_node in cytoscape_compound_elements['nodes']:
        #    print(temp_node['data'])    
            if temp_node['data']['id'] in store_compound_data['compounds']:
                #if temp_node['classes']=='selected':
                #    temp_node['classes']='not_selected'
                #elif temp_node['classes']=='not_selected':
                temp_node['classes']='selected' 

        checkbox_values=[]
        #if (('22' in store_compound_data) and ('5' in store_compound_data)):
        #    checkbox_values.append('both_glucoses')        
        for temp_checkbox in checklist_hashmap.keys():
            #if every node id is in the store
            if all([(i in store_compound_data['compounds']) for i in checklist_hashmap[temp_checkbox]]):
                checkbox_values.append(temp_checkbox)
                store_compound_data['checkboxes'].append(temp_checkbox)


        temp_dropdown_values=store_compound_data['compounds']

        return cytoscape_compound_elements, checkbox_values, temp_dropdown_values,store_compound_data



# @app.callback(
#     [Output(component_id='div_cytoscape_compound_cyto',component_property='children')],
#     #gets n_clicks=0 when app loads, thats why you get a cyto right off the bat
#     [Input(component_id='button_add_cyto_compound',component_property='n_clicks')],
#     [State(component_id='div_cytoscape_compound_cyto',component_property='children'),
#     State(component_id='store_cyto_compound',component_property='data')],prevent_initial_callback=True
# )
# def add_cyto_compound(temp_n_clicks,temp_children,temp_store):

#     if (callback_context.triggered[0]['prop_id']=='.'):
#         for i,element in enumerate(temp_store):
#             new_graph=dbc.Row(
#                 dbc.Col(
#                     dbc.Card(
#                         children=[
#                             #compounds
#                             cyto.Cytoscape(
#                                 id={
#                                     'type':'cytoscape_compound',
#                                     'key':i
#                                 },
#                                 layout={'name':'dagre'},
#                                 elements=compound_network_dict['elements'],
#                                 stylesheet=stylesheet,
#                                 minZoom=0.3,
#                                 maxZoom=5
#                             )
#                         ]
#                     ),
#                     width='auto',
#                     align='center'
#                 )
#             )

#             temp_children.append(new_graph)


#     #if (callback_context.triggered[0]['prop_id']=='.'):

#     elif (callback_context.triggered[0]['prop_id']=='button_add_cyto_compound.n_clicks'):
#         temp_children.append(new_graph)

#     return [temp_children]

# @app.callback(
#     [Output(component_id={'type':'cytoscape_compound','key':MATCH},component_property='elements')],
#     [Input(component_id={'type':'cytoscape_compound','key':MATCH},component_property='tapNodeData')],
#     #Input(component_id='button_add_cyto_compound',component_property='n_clicks')],
#     #Input(component_id='Compounds',component_property='href')],
#     [State(component_id={'type':'cytoscape_compound','key':MATCH},component_property='elements'),
#     State(component_id='store_cyto_compound',component_property='data')]#,prevent_initial_call=True
# )
# def update_node_selection(temp_tap,temp_elements,temp_store):

#     if temp_tap is None:
#         raise PreventUpdate

#     elif callback_context.triggered[0]['prop_id']=='.':
#         raise PreventUpdate

#     try:
#         child_nodes_and_self=nx.algorithms.dag.descendants(networkx,temp_tap['id'])
#     except nx.NetworkXError:
#         child_nodes_and_self=set()

#     child_nodes_and_self.add(temp_tap['id'])

#     child_nodes_and_self=set(map(str,child_nodes_and_self))

#     for temp_node in temp_elements['nodes']:

#         if temp_node['data']['id'] in child_nodes_and_self:


#             if temp_node['classes']=='selected':
#                 temp_node['classes']='not_selected'
#             elif temp_node['classes']=='not_selected':
#                 temp_node['classes']='selected'

#     return [temp_elements]


# def check_if_selected(temp_dict):

#     if temp_dict['classes']=='selected':
#         return str(temp_dict['data']['id'])


# @app.callback(
#     [Output(component_id='store_cyto_compound',component_property='data')],
#     [Input(component_id={'type':'cytoscape_compound','key':ALL},component_property='elements')],
#     [State(component_id='store_cyto_compound',component_property='data')]
#     ,prevent_initial_call=True
# )
# def add_selections_to_store(temp_elements,temp_store):

    

#     print('\nadd_selections_to_store')
#     print(callback_context.triggered[0]['prop_id'])
#     #print(temp_elements)

#     if callback_context.triggered[0]['prop_id']=='.':
#         raise PreventUpdate

#     selected_ids_list=[list(map(check_if_selected,temp_cyto_dict['nodes'])) for temp_cyto_dict in temp_elements]

    
#     return [selected_ids_list]
