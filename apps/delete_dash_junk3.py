dash_layout_components = {
    'time_slider_app2': 'value',
    'backtest_choice_app2': 'values',
    'asset_selection_app2': 'value',
    'graph_selection_app2': 'values'
}

set_back_and_display_graph_input = {
    'store_layout_data': 'modified_timestamp',
    'tabs': 'value'
}


@app.callback(
    Output('store_layout_data', 'data'),
    [Input(key, value) for key, value in dash_layout_components.items()]
)
def store_layout(time_slider_value, backtest_choice_values, assets_selection_values, graph_selection_values):

    data_json = {
        'time_slider_value': time_slider_value,
        'backtest_choice_values': backtest_choice_values,
        'asset_selection_value': assets_selection_values,
        'graph_selection_values': graph_selection_values
    }
    return data_json


@app.callback(
    Output('store_layout_data', 'clear_data'),
    [Input('bt_erase_layout_storage_app2', 'n_clicks_timestamp')],
    [State('tabs', 'value')]
)
def erase_layout_data(bouton_ts, tab_value):

    if tab_value != '/app2':
        raise PreventUpdate
    return True


for component_id, component_property in dash_layout_components.items():
    @app.callback(
        Output(component_id, component_property),
        [Input(key, value) for key, value in set_back_and_display_graph_input.items()],
        [State('store_layout_data', 'data'), 
         State(component_id, 'id')]
    )
    def set_back_component(bouton_ts, tabs_value, layout_state_data, component):  
        if tabs_value != '/app2':
           raise PreventUpdate

        if layout_state_data is None:
            return []

        else:
            stored_layout_value_name = [key[:key.rfind('a')] + value for key, value in dash_layout_components.items()]
            store_layout_component_name = stored_layout_value_name[list(dash_layout_components.keys()).index(component)]
            return layout_state_data[store_layout_component_name]