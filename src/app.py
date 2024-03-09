from dash import Dash, html,dcc, Input,Output, State
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import sqlite3
import json

from figures import *

course_index=find_course_index('design studies',1)

pie_chart=generate_pie_chart(course_index)
satisfaction_indicators=generate_satisfaction_indicators(course_index)
bar_chart=generate_bar_chart(course_index,3,['UK'])

#Establish connection with sqlite database
sqliteConnection = sqlite3.connect('database.sqlite',check_same_thread=False)
cursor = sqliteConnection.cursor()

#Select column with course names from course table in database.sqlite
query = 'SELECT COURSE FROM course;'
cursor.execute(query)
result = cursor.fetchall()
# Convert selected course names into json format
result_json=json.dumps(result)
# Convert json format into pandas object (df)
result_pd=pd.read_json(result_json)
# Remove course name duplicates (in the table they are not really dups bc although it's the same course_name, they have different study modes)
result_pd=result_pd.drop_duplicates()

# Append a list opt with course names in the format expected by the dropdown options
opt=[]
for row in range(len(result_pd)):
    course_name=result_pd.iloc[row,0]
    opt.append({'label': course_name, 'value': course_name})


# Variable that contains the external_stylesheet to use (ie.Flatly styling from dash bootstrap components (dbc))
external_stylesheets = [dbc.themes.LITERA]

# Variable that contains the meta tags (to ensure responsive design)
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__,external_stylesheets=external_stylesheets,meta_tags=meta_tags)

# Define the three rows of the app layout 
row_one = html.Div(
        dbc.Row([
        dbc.Col([html.H1("Welcome to GRAD:ME! Dashboard", id='app_header'), 
                 html.P("Find all the infomation you need regarding employment prospects after graduation in ONE SINGLE PAGE !", id="first_paragraph_row1"),
                 ], width={"size": 12}),
    ]),
)

row_two = html.Div(
    dbc.Row([
        dbc.Col(children=[dbc.Label("Select your course"), 
                          dbc.Select(id="course_name_select",
                                     # id uniquely identifies the element, will be needed later
                                     #value="COURSE 1",  # The default selection,
                                     #id="course_name_selector"
                                     options=opt,
                                     value='design studies'
                                     ),
                          ], width=4),
        dbc.Col(children=[dbc.Label("Select your study mode"), 
                          dbc.RadioItems(
                            options=[
                                {"label": "Full-Time", "value": 1},
                                {"label": "Part-Time", "value": 2}
                            ],
                            value=1,
                            id="kis_mode_select")],
                            width=4),
        dbc.Col(children=[dbc.Label("Select your kis level"), 
                    dbc.RadioItems(
                    options=[
                        {"label": "3", "value": 3},
                        {"label": "4", "value": 4}
                    ],
                    value=3,
                    id="kis_level_select")],
                    width=4)
    ]),
)

row_three = html.Div(
    dbc.Row([
        dbc.Col(dcc.Graph(id="pie_chart",figure=pie_chart)),
        dbc.Col(dcc.Graph(id="satisfaction_indicators",figure=satisfaction_indicators))
                 ])
)

row_four = html.Div(
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar_chart",figure=bar_chart)),
        dbc.Col(children=[dbc.Label("Select the countries you would like to work in"), 
                         dbc.Checklist(
                        options=[
                            {'label': 'United Kingdom', 'value': 'UK'},
                            {'label': 'England', 'value': 'England'},
                            {'label': 'Scotland', 'value': 'Scotland'},
                            {'label': 'Wales', 'value': 'Wales'},
                            {'label': 'Northern Ireland', 'value': 'NI'}
                        ],
                        value=['UK'],
                        id='countries_select'
    )]),
    ])
    )

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
        Input(component_id="kis_level_select",component_property="value"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value")
        ]
)

@app.callback(
        Output(component_id="satisfaction_indicators",component_property="figure"),
        #trigger the callback/figure update once the kis_level is selected
        Input(component_id="kis_level_select",component_property="value"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value")
        ]
)

@app.callback(
        Output(component_id="bar_chart",component_property="figure"),
        #trigger the callback/figure update once the kis_level is selected
        Input(component_id="countries_select",component_property="value"),
        [
            State("course_name_select","value"),
            State("kis_mode_select", "value"),
            State("kis_level_select", "value")
        ]
)

def update_pie_chart(input1,input2,input3):
    course_index=find_course_index(input2,input3)
    pie_chart=generate_pie_chart(course_index)
    return pie_chart

def update_satisfaction_indicators(input1,input2,input3):
    course_index=find_course_index(input2,input3)
    satisfaction_indicators=generate_satisfaction_indicators(course_index)
    return satisfaction_indicators

def update_bar_chart(input1,input2,input3,input4):
    course_index=find_course_index(input2,input3)
    bar_chart=generate_bar_chart(course_index,input4,input1)
    return bar_chart
# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
    # Runs on port 8050 by default. If you have a port conflict, add the parameter port=   e.g. port=8051
