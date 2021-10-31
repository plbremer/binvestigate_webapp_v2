from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
from dash import callback_context

# Connect to main app.py file
from app import app
#from app import server
from apps import cyto_compound
from apps import backend_dataset
from apps import additional_filters



app.layout = html.Div(
    [
        #storage_type='session',
        dcc.Store(id='store_compound'),
        
        dbc.Row(
            #for the moment, we put all in one column
            #but maybe later put in separate columns
            #just put one of each link into a different column
            dbc.Col(
                html.Div(
                    children=[
                        dcc.Location(id='url',pathname='',refresh=False),
                        dcc.Link('Compounds',href='/apps/cyto_compound'),
                        dcc.Link('Backend Dataset',href='/apps/backend_dataset'),
                        #dcc.Link('Additional Filters',href='/apps/additional_filters')
                    ]
                ),

            )
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id='page_content',
                    children=[]
                )
            )
        )
    ]
)

@app.callback(
    [Output(component_id='page_content',component_property='children')],
    [Input(component_id='url',component_property='pathname')]
)
def display_page(temp_pathname):
    if temp_pathname == '/apps/cyto_compound':
        return [cyto_compound.layout]
    elif temp_pathname == '/apps/backend_dataset':
        return [backend_dataset.layout]
    #elif temp_pathname == '/apps/additional_filters':
    #    return [additional_filters.layout]


    else:
        return 'under construction'


if __name__ == '__main__':
    app.run_server(debug=True)