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


#load the base species network
species_json_address=DATA_PATH.joinpath('cyto_format_species.json')
temp_json_file=open(species_json_address,'r')
species_network_dict=json.load(temp_json_file)
temp_json_file.close()
for temp_element in species_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name species
    #try:
    temp_element['data']['label']=temp_element['data']['scientific_name']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'


#load the base organ network
organ_json_address=DATA_PATH.joinpath('cyto_format_organ.json')
temp_json_file=open(organ_json_address,'r')
organ_network_dict=json.load(temp_json_file)
temp_json_file.close()
for temp_element in organ_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name organ
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'


#load the base disease network
disease_json_address=DATA_PATH.joinpath('cyto_format_disease.json')
temp_json_file=open(disease_json_address,'r')
disease_network_dict=json.load(temp_json_file)
temp_json_file.close()
for temp_element in disease_network_dict['elements']['nodes']:
    #id and label are special keys for cytoscape dicts
    #they are always expected. our conversion script makes the id but does not make the name
    #so we add it manually here
    #we do not know how we intend to name disease
    #try:
    temp_element['data']['label']=temp_element['data']['mesh_label']
    #except KeyError:
    #    temp_element['data']['label']=temp_element['data']['name']
    temp_element['classes']='not_selected'


#defines the map between the various boxes and the node ids
checklist_hashmap_species={
    'primed apes': ['9606','10090','314146'],
    'some plant':['3701','72658']
}

#defines the map between the various boxes and the node ids
checklist_hashmap_organ={
    'junk': ['A01'],
}

#defines the map between the various boxes and the node ids
checklist_hashmap_disease={
    'junk': ['C01'],
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

#might want to put this in index?
networkx_address_species=DATA_PATH.joinpath('species_networkx.bin')
networkx_species=nx.readwrite.gpickle.read_gpickle(networkx_address_species)

networkx_address_organ=DATA_PATH.joinpath('organ_networkx.bin')
networkx_organ=nx.readwrite.gpickle.read_gpickle(networkx_address_organ)

networkx_address_disease=DATA_PATH.joinpath('disease_networkx.bin')
networkx_disease=nx.readwrite.gpickle.read_gpickle(networkx_address_disease)

layout=html.Div(
    children=[
        html.Div(
            id='div_cytoscape_species_cyto',
            children=[
                cyto.Cytoscape(
                    id='cytoscape_species',
                    layout={'name':'dagre'},
                    elements=species_network_dict['elements'],
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
                                id='checklist_species',
                                options=[
                                    {'label': i, 'value': i} for i in checklist_hashmap_species.keys()
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
                                id='dropdown_species',
                                options=[
                                    {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in species_network_dict['elements']['nodes']
                                ],
                                multi=True
                            )
                        ],
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
                                id='button_species',
                            )
                        ],
                    )
                ),
            ]
        ),

        html.Div(
            id='div_cytoscape_organ_cyto',
            children=[
                cyto.Cytoscape(
                    id='cytoscape_organ',
                    layout={'name':'dagre'},
                    elements=organ_network_dict['elements'],
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
                                id='checklist_organ',
                                options=[
                                    {'label': i, 'value': i} for i in checklist_hashmap_organ.keys()
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
                                id='dropdown_organ',
                                options=[
                                    {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in organ_network_dict['elements']['nodes']
                                ],
                                multi=True
                            )
                        ],
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
                                id='button_organ',
                            )
                        ],
                    )
                ),
            ]
        ),

        html.Div(
            id='div_cytoscape_disease_cyto',
            children=[
                cyto.Cytoscape(
                    id='cytoscape_disease',
                    layout={'name':'dagre'},
                    elements=disease_network_dict['elements'],
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
                                id='checklist_disease',
                                options=[
                                    {'label': i, 'value': i} for i in checklist_hashmap_disease.keys()
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
                                id='dropdown_disease',
                                options=[
                                    {'label': temp_node['data']['label'], 'value': temp_node['data']['id']} for temp_node in disease_network_dict['elements']['nodes']
                                ],
                                multi=True
                            )
                        ],
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
                                id='button_disease',
                            )
                        ],
                    )
                ),
            ]
        ),

    ]
)


@app.callback(
    [Output(component_id='cytoscape_species',component_property='elements'),
    Output(component_id='checklist_species',component_property='value'),
    Output(component_id='dropdown_species',component_property='value'),
    Output(component_id='store_from_species',component_property='data')],
    
    [Input(component_id='cytoscape_species',component_property='tapNodeData'),
    Input(component_id='checklist_species',component_property='value'),
    Input(component_id='dropdown_species',component_property='value'),
    Input(component_id='button_species',component_property='n_clicks')],
    
    [State(component_id='cytoscape_species',component_property='elements'),
    State(component_id='store_from_species',component_property='data')]
)
def callback_aggregate(
    cytoscape_species_tapnodedata,
    checklist_species_value,
    dropdown_species_value,
    button_species_value,

    cytoscape_species_elements,
    store_from_species_data
):

    if (len(callback_context.triggered)>1) and (store_from_species_data is None):

        store_from_species_data={
            'species':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_species_value=list()

        return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data

    elif (len(callback_context.triggered)>1) and (store_from_species_data is not None):
        cytoscape_species_elements, 
        for temp_node in cytoscape_species_elements['nodes']:
            if temp_node['data']['id'] in store_from_species_data['species']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
                      
        dropdown_species_value=store_from_species_data['species']

        checklist_species_value=store_from_species_data['checkboxes']

        #dont do anthing to store_from_species_data

        return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_species.tapNodeData'):
        
        #elements
        try:
            child_nodes_and_self=nx.algorithms.dag.descendants(networkx_species,cytoscape_species_tapnodedata['id'])
        except nx.NetworkXError:
            child_nodes_and_self=set()
        child_nodes_and_self.add(cytoscape_species_tapnodedata['id'])
        child_nodes_and_self=set(map(str,child_nodes_and_self))
        
        for temp_node in cytoscape_species_elements['nodes']:
            if temp_node['data']['id'] in child_nodes_and_self:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store species
        new_species_list=list()
        for temp_node in cytoscape_species_elements['nodes']:
            if temp_node['classes']=='selected':
                new_species_list.append(temp_node['data']['id'])        
        store_from_species_data['species']=new_species_list

        #dropdown
        dropdown_species_value=store_from_species_data['species']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_species.keys():
            #if every node id is in the store
            if all([(i in store_from_species_data['species']) for i in checklist_hashmap_species[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_species_value=new_checkbox_values

        #store checkboxes        
        store_from_species_data['checkboxes']=checklist_species_value

        return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_species.value'):

        if (len(store_from_species_data['checkboxes']) < len(checklist_species_value)):

            box_we_clicked=list(set(checklist_species_value).difference(set(store_from_species_data['checkboxes'])))[0]

            #elements
            for temp_node in cytoscape_species_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_species[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_from_species_data['checkboxes'].append(box_we_clicked)
            store_from_species_data['species']=list(set(store_from_species_data['species']).union(set(checklist_hashmap_species[box_we_clicked])))

            #dropdown
            dropdown_species_value=store_from_species_data['species']
            
            return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data
           
        elif len(store_from_species_data['checkboxes']) > len(checklist_species_value):

            box_we_unclicked=list(set(store_from_species_data['checkboxes']).difference(set(checklist_species_value)))[0]

            #elements
            for temp_node in cytoscape_species_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_species[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_from_species_data['checkboxes'].remove(box_we_unclicked)
            store_from_species_data['species']=list(set(store_from_species_data['species']).difference(set(checklist_hashmap_species[box_we_unclicked])))

            #dropdown
            dropdown_species_value=store_from_species_data['species']

            return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_species.value'):

        if len(store_from_species_data['species']) < len(dropdown_species_value):

            species_we_added=list(set(dropdown_species_value).difference(set(store_from_species_data['species'])))[0]

            #elements
            for temp_node in cytoscape_species_elements['nodes']:
                if temp_node['data']['id'] == species_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_from_species_data['species'].append(species_we_added)

            #so the general logic is
            #we chose a species
            #that species belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of species is selected (the currently chosen species)
            #being the "completing species"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_species_belongs=list()
            checkboxes_to_which_this_species_belongs=[temp_key for temp_key in checklist_hashmap_species.keys() if (species_we_added in checklist_hashmap_species[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_species_belongs:
                #if the set of species implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of species is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_species[temp_checkbox]).difference(set(dropdown_species_value)))==0:
                    store_from_species_data['checkboxes'].append(temp_checkbox)
                    checklist_species_value.append(temp_checkbox)

            return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data

        elif len(store_from_species_data['species']) > len(dropdown_species_value):

            species_we_lost=list(set(store_from_species_data['species']).difference(set(dropdown_species_value)))[0]

            #elements
            for temp_node in cytoscape_species_elements['nodes']:
                if temp_node['data']['id'] == species_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_from_species_data['species'].remove(species_we_lost)

            #checklist
            #so the general logic is
            #we chose a species
            #that species belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of species is selected (the currently chosen species)
            #being the "completing species"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_species_belongs=list()
            checkboxes_to_which_this_species_belongs=[temp_key for temp_key in checklist_hashmap_species.keys() if (species_we_lost in checklist_hashmap_species[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_species_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_from_species_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_species_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_species.n_clicks'):

        store_from_species_data={
            'species':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_species_elements['nodes']:
            temp_node['classes']='not_selected'  

        checklist_species_value=list()

        dropdown_species_value=None

        return cytoscape_species_elements, checklist_species_value, dropdown_species_value,store_from_species_data




@app.callback(
    [Output(component_id='cytoscape_organ',component_property='elements'),
    Output(component_id='checklist_organ',component_property='value'),
    Output(component_id='dropdown_organ',component_property='value'),
    Output(component_id='store_from_organ',component_property='data')],
    
    [Input(component_id='cytoscape_organ',component_property='tapNodeData'),
    Input(component_id='checklist_organ',component_property='value'),
    Input(component_id='dropdown_organ',component_property='value'),
    Input(component_id='button_organ',component_property='n_clicks')],
    
    [State(component_id='cytoscape_organ',component_property='elements'),
    State(component_id='store_from_organ',component_property='data')]
)
def callback_aggregate(
    cytoscape_organ_tapnodedata,
    checklist_organ_value,
    dropdown_organ_value,
    button_organ_value,

    cytoscape_organ_elements,
    store_from_organ_data
):

    if (len(callback_context.triggered)>1) and (store_from_organ_data is None):

        store_from_organ_data={
            'organ':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_organ_value=list()

        return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data

    elif (len(callback_context.triggered)>1) and (store_from_organ_data is not None):
        cytoscape_organ_elements, 
        for temp_node in cytoscape_organ_elements['nodes']:
            if temp_node['data']['id'] in store_from_organ_data['organ']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
                      
        dropdown_organ_value=store_from_organ_data['organ']

        checklist_organ_value=store_from_organ_data['checkboxes']

        #dont do anthing to store_from_organ_data

        return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_organ.tapNodeData'):
        
        #elements
        try:
            child_nodes_and_self=nx.algorithms.dag.descendants(networkx_organ,cytoscape_organ_tapnodedata['id'])
        except nx.NetworkXError:
            child_nodes_and_self=set()
        child_nodes_and_self.add(cytoscape_organ_tapnodedata['id'])
        child_nodes_and_self=set(map(str,child_nodes_and_self))
        
        for temp_node in cytoscape_organ_elements['nodes']:
            if temp_node['data']['id'] in child_nodes_and_self:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store organ
        new_organ_list=list()
        for temp_node in cytoscape_organ_elements['nodes']:
            if temp_node['classes']=='selected':
                new_organ_list.append(temp_node['data']['id'])        
        store_from_organ_data['organ']=new_organ_list

        #dropdown
        dropdown_organ_value=store_from_organ_data['organ']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_organ.keys():
            #if every node id is in the store
            if all([(i in store_from_organ_data['organ']) for i in checklist_hashmap_organ[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_organ_value=new_checkbox_values

        #store checkboxes        
        store_from_organ_data['checkboxes']=checklist_organ_value

        return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_organ.value'):

        if (len(store_from_organ_data['checkboxes']) < len(checklist_organ_value)):

            box_we_clicked=list(set(checklist_organ_value).difference(set(store_from_organ_data['checkboxes'])))[0]

            #elements
            for temp_node in cytoscape_organ_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_organ[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_from_organ_data['checkboxes'].append(box_we_clicked)
            store_from_organ_data['organ']=list(set(store_from_organ_data['organ']).union(set(checklist_hashmap_organ[box_we_clicked])))

            #dropdown
            dropdown_organ_value=store_from_organ_data['organ']
            
            return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data
           
        elif len(store_from_organ_data['checkboxes']) > len(checklist_organ_value):

            box_we_unclicked=list(set(store_from_organ_data['checkboxes']).difference(set(checklist_organ_value)))[0]

            #elements
            for temp_node in cytoscape_organ_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_organ[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_from_organ_data['checkboxes'].remove(box_we_unclicked)
            store_from_organ_data['organ']=list(set(store_from_organ_data['organ']).difference(set(checklist_hashmap_organ[box_we_unclicked])))

            #dropdown
            dropdown_organ_value=store_from_organ_data['organ']

            return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_organ.value'):

        if len(store_from_organ_data['organ']) < len(dropdown_organ_value):

            organ_we_added=list(set(dropdown_organ_value).difference(set(store_from_organ_data['organ'])))[0]

            #elements
            for temp_node in cytoscape_organ_elements['nodes']:
                if temp_node['data']['id'] == organ_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_from_organ_data['organ'].append(organ_we_added)

            #so the general logic is
            #we chose a organ
            #that organ belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of organ is selected (the currently chosen organ)
            #being the "completing organ"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_organ_belongs=list()
            checkboxes_to_which_this_organ_belongs=[temp_key for temp_key in checklist_hashmap_organ.keys() if (organ_we_added in checklist_hashmap_organ[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_organ_belongs:
                #if the set of organ implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of organ is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_organ[temp_checkbox]).difference(set(dropdown_organ_value)))==0:
                    store_from_organ_data['checkboxes'].append(temp_checkbox)
                    checklist_organ_value.append(temp_checkbox)

            return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data

        elif len(store_from_organ_data['organ']) > len(dropdown_organ_value):

            organ_we_lost=list(set(store_from_organ_data['organ']).difference(set(dropdown_organ_value)))[0]

            #elements
            for temp_node in cytoscape_organ_elements['nodes']:
                if temp_node['data']['id'] == organ_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_from_organ_data['organ'].remove(organ_we_lost)

            #checklist
            #so the general logic is
            #we chose a organ
            #that organ belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of organ is selected (the currently chosen organ)
            #being the "completing organ"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_organ_belongs=list()
            checkboxes_to_which_this_organ_belongs=[temp_key for temp_key in checklist_hashmap_organ.keys() if (organ_we_lost in checklist_hashmap_organ[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_organ_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_from_organ_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_organ_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_organ.n_clicks'):

        store_from_organ_data={
            'organ':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_organ_elements['nodes']:
            temp_node['classes']='not_selected'  

        checklist_organ_value=list()

        dropdown_organ_value=None

        return cytoscape_organ_elements, checklist_organ_value, dropdown_organ_value,store_from_organ_data



@app.callback(
    [Output(component_id='cytoscape_disease',component_property='elements'),
    Output(component_id='checklist_disease',component_property='value'),
    Output(component_id='dropdown_disease',component_property='value'),
    Output(component_id='store_from_disease',component_property='data')],
    
    [Input(component_id='cytoscape_disease',component_property='tapNodeData'),
    Input(component_id='checklist_disease',component_property='value'),
    Input(component_id='dropdown_disease',component_property='value'),
    Input(component_id='button_disease',component_property='n_clicks')],
    
    [State(component_id='cytoscape_disease',component_property='elements'),
    State(component_id='store_from_disease',component_property='data')]
)
def callback_aggregate(
    cytoscape_disease_tapnodedata,
    checklist_disease_value,
    dropdown_disease_value,
    button_disease_value,

    cytoscape_disease_elements,
    store_from_disease_data
):

    if (len(callback_context.triggered)>1) and (store_from_disease_data is None):

        store_from_disease_data={
            'disease':[],
            'checkboxes':[]
        }
        
        #without this we get 
        #Cannot read properties of null (reading 'indexOf')
        #https://stackoverflow.com/questions/62183202/cannot-read-properly-data-of-null-dash
        checklist_disease_value=list()

        return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data

    elif (len(callback_context.triggered)>1) and (store_from_disease_data is not None):
        cytoscape_disease_elements, 
        for temp_node in cytoscape_disease_elements['nodes']:
            if temp_node['data']['id'] in store_from_disease_data['disease']:
                temp_node['classes']='selected'
            else:
                temp_node['classes']='not_selected'
                      
        dropdown_disease_value=store_from_disease_data['disease']

        checklist_disease_value=store_from_disease_data['checkboxes']

        #dont do anthing to store_from_disease_data

        return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='cytoscape_disease.tapNodeData'):
        
        #elements
        try:
            child_nodes_and_self=nx.algorithms.dag.descendants(networkx_disease,cytoscape_disease_tapnodedata['id'])
        except nx.NetworkXError:
            child_nodes_and_self=set()
        child_nodes_and_self.add(cytoscape_disease_tapnodedata['id'])
        child_nodes_and_self=set(map(str,child_nodes_and_self))
        
        for temp_node in cytoscape_disease_elements['nodes']:
            if temp_node['data']['id'] in child_nodes_and_self:
                if temp_node['classes']=='selected':
                    temp_node['classes']='not_selected'
                elif temp_node['classes']=='not_selected':
                    temp_node['classes']='selected'   

        #store disease
        new_disease_list=list()
        for temp_node in cytoscape_disease_elements['nodes']:
            if temp_node['classes']=='selected':
                new_disease_list.append(temp_node['data']['id'])        
        store_from_disease_data['disease']=new_disease_list

        #dropdown
        dropdown_disease_value=store_from_disease_data['disease']

        #checkbox
        new_checkbox_values=list()
        for temp_checkbox in checklist_hashmap_disease.keys():
            #if every node id is in the store
            if all([(i in store_from_disease_data['disease']) for i in checklist_hashmap_disease[temp_checkbox]]):
                new_checkbox_values.append(temp_checkbox)
        checklist_disease_value=new_checkbox_values

        #store checkboxes        
        store_from_disease_data['checkboxes']=checklist_disease_value

        return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='checklist_disease.value'):

        if (len(store_from_disease_data['checkboxes']) < len(checklist_disease_value)):

            box_we_clicked=list(set(checklist_disease_value).difference(set(store_from_disease_data['checkboxes'])))[0]

            #elements
            for temp_node in cytoscape_disease_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_disease[box_we_clicked]:
                    temp_node['classes']='selected'  

            #store
            store_from_disease_data['checkboxes'].append(box_we_clicked)
            store_from_disease_data['disease']=list(set(store_from_disease_data['disease']).union(set(checklist_hashmap_disease[box_we_clicked])))

            #dropdown
            dropdown_disease_value=store_from_disease_data['disease']
            
            return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data
           
        elif len(store_from_disease_data['checkboxes']) > len(checklist_disease_value):

            box_we_unclicked=list(set(store_from_disease_data['checkboxes']).difference(set(checklist_disease_value)))[0]

            #elements
            for temp_node in cytoscape_disease_elements['nodes']:
                if temp_node['data']['id'] in checklist_hashmap_disease[box_we_unclicked]:
                    temp_node['classes']='not_selected' 

            #store
            store_from_disease_data['checkboxes'].remove(box_we_unclicked)
            store_from_disease_data['disease']=list(set(store_from_disease_data['disease']).difference(set(checklist_hashmap_disease[box_we_unclicked])))

            #dropdown
            dropdown_disease_value=store_from_disease_data['disease']

            return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='dropdown_disease.value'):

        if len(store_from_disease_data['disease']) < len(dropdown_disease_value):

            disease_we_added=list(set(dropdown_disease_value).difference(set(store_from_disease_data['disease'])))[0]

            #elements
            for temp_node in cytoscape_disease_elements['nodes']:
                if temp_node['data']['id'] == disease_we_added:
                    temp_node['classes']='selected'  
                    break
            
            #store
            store_from_disease_data['disease'].append(disease_we_added)

            #so the general logic is
            #we chose a disease
            #that disease belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of disease is selected (the currently chosen disease)
            #being the "completing disease"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_disease_belongs=list()
            checkboxes_to_which_this_disease_belongs=[temp_key for temp_key in checklist_hashmap_disease.keys() if (disease_we_added in checklist_hashmap_disease[temp_key])]

            for temp_checkbox in checkboxes_to_which_this_disease_belongs:
                #if the set of disease implied by temp_checkbox is in the store/elements
                #then add the chceklist to the store/add the value to the checklist values
                #we can check is the set of disease is there by doing a difference and if the difference length is zero
                if len(set(checklist_hashmap_disease[temp_checkbox]).difference(set(dropdown_disease_value)))==0:
                    store_from_disease_data['checkboxes'].append(temp_checkbox)
                    checklist_disease_value.append(temp_checkbox)

            return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data

        elif len(store_from_disease_data['disease']) > len(dropdown_disease_value):

            disease_we_lost=list(set(store_from_disease_data['disease']).difference(set(dropdown_disease_value)))[0]

            #elements
            for temp_node in cytoscape_disease_elements['nodes']:
                if temp_node['data']['id'] == disease_we_lost:
                    temp_node['classes']='not_selected'  
                    break
            
            #store
            store_from_disease_data['disease'].remove(disease_we_lost)

            #checklist
            #so the general logic is
            #we chose a disease
            #that disease belongs to some number of checkboxes (we can check membership in each checkbox
            #for checkbox that it belongs to, we must check whether the entire set of disease is selected (the currently chosen disease)
            #being the "completing disease"
            #if this is true, then we 1) add that checkbox to the store checkboxes and 2) add that checkbox to the checkbox values
            #checkboxes_to_which_this_disease_belongs=list()
            checkboxes_to_which_this_disease_belongs=[temp_key for temp_key in checklist_hashmap_disease.keys() if (disease_we_lost in checklist_hashmap_disease[temp_key])]
            for temp_checkbox in checkboxes_to_which_this_disease_belongs:
                #this is easier than adding checkboxes
                #now, if a checkbox is in store or the checkbox list
                #just remove that checkbox
                try:
                    store_from_disease_data['checkboxes'].remove(temp_checkbox)
                except ValueError:
                    continue
                try:
                    checklist_disease_value.remove(temp_checkbox)
                except ValueError:
                    continue

            return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data

    elif (len(callback_context.triggered)==1) and (callback_context.triggered[0]['prop_id']=='button_disease.n_clicks'):

        store_from_disease_data={
            'disease':[],
            'checkboxes':[]
        }

        for temp_node in cytoscape_disease_elements['nodes']:
            temp_node['classes']='not_selected'  

        checklist_disease_value=list()

        dropdown_disease_value=None

        return cytoscape_disease_elements, checklist_disease_value, dropdown_disease_value,store_from_disease_data