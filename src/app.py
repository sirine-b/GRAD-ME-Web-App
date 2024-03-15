from dash import Dash, html,dcc, Input,Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
import json

from figures import *
from layout_app import *

# Variable that contains the external_stylesheet to use (ie.Flatly styling from dash bootstrap components (dbc))
external_stylesheets = [dbc.themes.LUMEN]

# Variable that contains the meta tags (to ensure responsive design)
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__,external_stylesheets=external_stylesheets,meta_tags=meta_tags)

# Add an HTML layout to the Dash app.
# The layout is wrapped in a DBC Container()
app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four
])

@app.callback(
        Output(component_id="pie_chart",component_property="figure"),
        #trigger the callback/figure update once the kis_level is selected
        Input("search_button","n_clicks"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value")
        ]
)

def update_pie_chart(input1,input2,input3):
    course_index=find_course_index(input2,input3)
    pie_chart=generate_pie_chart(course_index)
    return pie_chart

@app.callback(
        Output(component_id="satisfaction_indicators",component_property="figure"),
        #trigger the callback/figure update once the kis_level is selected
        Input("search_button","n_clicks"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value")
        ]
)
def update_satisfaction_indicators(input1,input2,input3):
    course_index=find_course_index(input2,input3)
    satisfaction_indicators=generate_satisfaction_indicators(course_index)
    return satisfaction_indicators

@app.callback(
        Output(component_id="bar_chart",component_property="figure"),
        #trigger the callback/figure update once the kis_level is selected
        Input("search_button","n_clicks"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value"),
            State("kis_level_select", "value"),
            State("countries_select", "value")
        ]
)

def update_bar_chart(input1,input2,input3,input4,input5):
    print(input4,input5)
    course_index=find_course_index(input2,input3)
    bar_chart=generate_bar_chart(course_index,input4,input5)
    return bar_chart

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
    # Runs on port 8050 by default. 
