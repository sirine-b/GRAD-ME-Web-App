from dash import html,dcc
import dash_bootstrap_components as dbc
import pandas as pd
import sqlite3
import json
import plotly.express as px


from src.figures import *
#from app import*

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
result_pd=pd.read_json(StringIO(result_json))
# Remove course name duplicates (in the table they are not really dups bc although it's the same course_name, they have different study modes)
result_pd=result_pd.drop_duplicates()

# Append a list opt with course names in the format expected by the dropdown options
opt=[]
for row in range(len(result_pd)):
    course_name=result_pd.iloc[row,0]
    opt.append({'label': course_name, 'value': course_name})

image_path='assets\info_tooltip_logo.png'

# Define the four rows of the app layout 
row_one = html.Div(
        dbc.Row([
        dbc.Col([html.H1("Welcome to GRAD:ME! Dashboard !!!", id='app_header', style={'font-family': 'Fantasy',\
                                                'color':px.colors.sequential.Burgyl[3],'padding-left':'70px'}),
                 dbc.Alert(["About to graduate and nervous about what's to come? Worry no more!", html.Br(),\
                         "Find all the infomation you need regarding employment prospects",html.Br(),
                        "post graduation on our single page GRAD:ME! Dashboard!"], \
                            id="intro_text",style={'font-size':18,'font-weight':'bold','left':'60px','width':'600px'},color=px.colors.sequential.Burgyl[3]),
                 ],width=8),
        dbc.Col([html.Div(
            id="errors")])
    ]),
)

row_two = html.Div(
    dbc.Row([
        dbc.Col(children=[dbc.Label("Select your course"), 
                          dbc.Select(id="course_name_select",
                                     options=opt,
                                     value='design studies'
                                     ),
                          ], width={"size": 4, "offset": 1}),
        dbc.Col(children=[dbc.Label("Select your study mode"), 
                          dbc.RadioItems(
                            options=[
                                {"label": "Full-Time", "value": 1},
                                {"label": "Part-Time", "value": 2}
                            ],
                            value=1,
                            id="kis_mode_select"),
                                ],
                            width=2),
        dbc.Col(children=[dbc.Label("Select your kis level",style={'float': 'left','height':'10px'}),
                          html.Div(html.Img(src=image_path,id='info_tooltip',style={'width': '35px','height':'20px'})) ,
                          dbc.RadioItems(
                            options=[
                                {"label": "3", "value": 3},
                                {"label": "4", "value": 4}
                    ],
                    value=3,
                    id="kis_level_select",
                    ),
                        dbc.Tooltip(
                            "Not sure what your course's kis level is?\
                            You can most likely find it on your course page\
                            through your university's website.",
                            target="info_tooltip",placement='right')],
                    width=2),
        dbc.Col(dbc.Button('Search!', id='search_button', n_clicks=0),
                style={'font-size': '15px', 'width': '140px', 'display': 'inline-block', 
                      'margin-bottom': '50px', 'margin-top': '30px', 'margin-right': '5px', 
                      'height':'25px'})
                      #className="d-grid gap-2 d-md-flex justify-content-md-end")
                      
    ]),
    #set space between this row and the previous one
    style={'height':'85px'}
)

row_three = html.Div(
    dbc.Row([
        dbc.Col(dcc.Graph(id="pie_chart",figure=pie_chart)),
        dbc.Col(dcc.Graph(id="satisfaction_indicators",figure=satisfaction_indicators))
                 ]),
        style={'height':'385px'}
)

row_four = html.Div(
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar_chart",figure=bar_chart),width=10),
        dbc.Col(children=[dbc.Label("Select the countries you would like to work in:"), 
                         dbc.Checklist(
                        options=[
                            {'label': 'United Kingdom', 'value': 'UK'},
                            {'label': 'England', 'value': 'England'},
                            {'label': 'Scotland', 'value': 'Scotland'},
                            {'label': 'Wales', 'value': 'Wales'},
                            {'label': 'Northern Ireland', 'value': 'NI'}
                        ],
                        value=['UK'],
                        id='countries_select'),
                        html.Div(id="no_countries_selected_error")
        ], style={'padding-top':'100px'})
    ])
    )