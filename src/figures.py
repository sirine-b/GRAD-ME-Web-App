from pathlib import Path
import sqlite3
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
                 title='What are graduates from your course doing?')
    #format figure's layout
    fig.update_layout(
    title_font_family="Times New Roman",
    title_font_size=30,
    title_font_color="black")
    fig.show()
generate_pie_chart('design studies', 2)

def generate_bar_chart(course_name, kis_mode):
    # Find course index (ie. FK) corresponding to the user-selected course name and kis_mode
    query="SELECT COURSE_INDEX FROM course WHERE COURSE='{}' and KISMODE='{}';".format(course_name, kis_mode)
    cursor.execute(query)
    result = cursor.fetchall()[0]
    result_json=json.dumps(result)
    result_pd=pd.read_json(result_json)
    course_index=result_pd[0][0]

    # Select satisfaction data (from satisfaction sqlite table) associated to the 
    # given course index (i.e. to the user-selected course name and study mode)
    query="SELECT STUDY,UNEMP,PREVWORKSTUD,BOTH,NOAVAIL,WORK FROM employment WHERE COURSE_INDEX='{}';".format(course_index)
    cursor.execute(query)
    result = cursor.fetchall()[0]
    result_json=json.dumps(result)
    result_df=pd.read_json(result_json)

    # Plot the pie chart
    labels=['Pursuing further studies','Unemployed','Worked AND/OR studied previously but not anymore','Both pursuing further studies AND working','Data not available','Working']
    fig = px.pie(result_df,values=0, names=labels,hole=0.4, color_discrete_sequence=px.colors.sequential.Burgyl,
                 title='What are graduates from your course doing?')
    #format figure's layout
    fig.update_layout(
    title_font_family="Times New Roman",
    title_font_size=30,
    title_font_color="black")
    fig.show()
generate_pie_chart('design studies', 2)

