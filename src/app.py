from dash import Dash, html,dcc, Input,Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
import json
from dash.exceptions import PreventUpdate
from dash.dash import no_update

from figures import *
from layout_elements import *

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

# def check_course_index(input1,input2,input3):
#     course_index=find_course_index(input2,input3)
#     if course_index=='error':
#         error = dbc.Alert("Sorry, no employment data is currently available for the selected course :(\
#                            We will try our best to add it to our database soon! In the meantime,\
#                            please select a different study mode, kis level or course name.")
#         return no_update,error
#     else:
#         error=''
#         return pie_chart,no_update

@app.callback(
        Output(component_id="pie_chart",component_property="figure"),
        Output(component_id="errors", component_property="children",allow_duplicate=True),
        #trigger the callback/figure update once the serach button is clicked
        Input("search_button","n_clicks"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value")
        ],
        prevent_initial_call=True,
)

def update_pie_chart(input1,input2,input3):
    course_index=find_course_index(input2,input3)
    pie_chart=generate_pie_chart(course_index)
    if pie_chart=='error':
        error = dbc.Alert("Sorry, no employment data is currently available for the selected course :(\
                           We will try our best to add it to our database soon! In the meantime,\
                           please select a different study mode, kis level or course name.")
        return no_update,error
    else:
        error=''
        return pie_chart,no_update

    return pie_chart

@app.callback(
        Output(component_id="satisfaction_indicators",component_property="figure"),
        Output(component_id="errors", component_property="children"),
        #trigger the callback/figure update once the search button is clicked
        Input("search_button","n_clicks"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value")
        ],
        prevent_initial_call=True,
)
def update_satisfaction_indicators(input1,input2,input3):
    course_index=find_course_index(input2,input3)
    satisfaction_indicators=generate_satisfaction_indicators(course_index)
    if satisfaction_indicators=='error':
        error = dbc.Alert("Sorry, no graduate satisfaction data is currently available for the selected course :(\
                           We will try our best to add it to our database soon! In the meantime,\
                           please select a different study mode, kis level or course name.")
        return no_update,error
    else:
        error=''
        return satisfaction_indicators,no_update

# Callback to update barcharts: 2 triggers => 1.when the user selects new countries 
# 2. when user clicks on search button (ie selects new course info)
@app.callback(
        Output(component_id="bar_chart",component_property="figure"),
        Output(component_id="errors",component_property="children",allow_duplicate=True),
        #trigger the callback/figure update once a new countries is selected/removed
        Input("countries_select","value"),
        Input("search_button","n_clicks"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value"),
            State("kis_level_select", "value"),
            State("countries_select", "value"),
            State("errors", "children")
        ],
        prevent_initial_call=True
)
def update_bar_chart(input1,input2,input3,input4,input5,input6,input7):
    course_index=find_course_index(input3,input4)
    bar_chart=generate_bar_chart(course_index,input5,input6)
    if bar_chart=='error':
        error = dbc.Alert("Sorry, no salary data is currently available for the selected course :(\
                           We will try our best to add it to our database soon! In the meantime,\
                           please select a different study mode, kis level or course name.")
        return no_update,error
    else:
        error=''
        return bar_chart,error


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)
    # Runs on port 8050 by default. 
