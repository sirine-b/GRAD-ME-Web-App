from pathlib import Path
import sqlite3
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Establish connection with sqlite database
sqliteConnection = sqlite3.connect('database.sqlite')
cursor = sqliteConnection.cursor()

def generate_pie_chart(course_name, kis_mode):

    # Find course index (ie. FK) corresponding to the user-selected course name and kis_mode
    query="SELECT COURSE_INDEX FROM course WHERE COURSE='{}' and KISMODE='{}';".format(course_name, kis_mode)
    cursor.execute(query)
    result = cursor.fetchall()[0]
    result_json=json.dumps(result)
    result_pd=pd.read_json(result_json)
    course_index=result_pd[0][0]

    # Select employment data (from employment sqlite table) associated to the 
    # given course index (i.e. to the user-selected course name and study mode)
    query="SELECT STUDY,UNEMP,PREVWORKSTUD,BOTH,NOAVAIL,WORK FROM employment WHERE COURSE_INDEX='{}';".format(course_index)
    cursor.execute(query)
    result = cursor.fetchall()[0]
    result_json=json.dumps(result)
    result_df=pd.read_json(result_json)

    # Plot the pie chart
    labels=['Pursuing further studies','Unemployed','Worked AND/OR studied previously but not anymore','Both pursuing further studies AND working','Data not available','Working']
    fig = px.pie(result_df,values=0, names=labels,hole=0.4, color_discrete_sequence=px.colors.sequential.Burgyl,
                 title='WHAT ARE GRADUATES FROM YOUR COURSE DOING?')
    #format figure's layout
    fig.update_layout(
    #title_font_family="Times New Roman",
    title_font_size=25,
    title_font_color="black",
    legend=dict(y=0.5),
    title=dict(x=0.5))
    fig.show()
generate_pie_chart('design studies', 2)

# Def margin between title and chart
mrg = dict(b = 100)
def generate_satisfaction_indicators(course_name, kis_mode):
    # Find course index (ie. FK) corresponding to the user-selected course name and kis_mode
    query="SELECT COURSE_INDEX FROM course WHERE COURSE='{}' and KISMODE='{}';".format(course_name, kis_mode)
    cursor.execute(query)
    result = cursor.fetchall()[0]
    result_json=json.dumps(result)
    result_df=pd.read_json(result_json)
    course_index=result_df[0][0]


    # Select satisfaction data (from satisfaction sqlite table) associated to the 
    # given course index (i.e. to the user-selected course name and study mode)
    query="SELECT GOWORKMEAN,GOWORKONTRACK,GOWORKSKILLS FROM satisfaction WHERE COURSE_INDEX='{}';".format(course_index)
    cursor.execute(query)
    result = cursor.fetchall()[0]
    result_json=json.dumps(result)
    result_df=pd.read_json(result_json)

    # Plot the indicators
    labels=['Agree or strongly agree that their current job is meaningful',
            'Agree or strongly agree that their current job fits their future plan',
            'Agree or strongly agree that they are using what they learnt in their studies in their current job']
    fig = go.Figure()
    fig.add_trace(go.Indicator(
    value = result_df[0][0],
    title = {'text': str(labels[0])},
    gauge = {'axis': {'range': [None, 100]},
             'bar': {'color': str(px.colors.sequential.Burgyl[0])}},
    domain = {'row': 0, 'column': 0}))
    
    fig.add_trace(go.Indicator(
    value = result_df[0][1],
    title = {'text': str(labels[1])},
    gauge = {'axis': {'range': [None, 100]},
             'bar': {'color': str(px.colors.sequential.Burgyl[2])}},
    domain = {'row': 1, 'column': 0}))

    fig.add_trace(go.Indicator(
    value = result_df[0][2],
    title = {'text': str(labels[2])},
    gauge = {'axis': {'range': [None, 100]},
             'bar': {'color': str(px.colors.sequential.Burgyl[4])}},
    domain = {'row': 2, 'column': 0}))

    fig.update_layout(
    grid = {'rows': 3, 'columns': 1, 'pattern': "independent"},
    template = {'data' : 
                {'indicator': [{
                'mode' : "number+gauge"}]
                }
                },
    title = {'text':'HOW DO GRADUATES FROM YOUR COURSE FEEL?',
             'x':0.5,
             'font':dict(size=25)},
    margin=mrg)
    fig.show()
generate_bar_chart('design studies',1)

