import dash
import dash_bootstrap_components as dbc

#import dash_cytoscape as cyto
#cyto.load_extra_layouts()

external_stylesheets = [dbc.themes.YETI]
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

server=app.server