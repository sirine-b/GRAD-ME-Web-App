from pathlib import Path
import sqlite3
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from threading import Lock
from io import StringIO
from dash.exceptions import PreventUpdate
#import dash
#from dash import html

# Establish connection with sqlite database
sqliteConnection = sqlite3.connect('database.sqlite',check_same_thread=False)
cursor = sqliteConnection.cursor()

lock=Lock()

def find_course_index(course_name, kis_mode):
    # Find course index (ie. FK) corresponding to the user-selected course name and kis_mode
    query="SELECT COURSE_INDEX FROM course WHERE COURSE='{}' and KISMODE='{}';".format(course_name, kis_mode)
    lock.acquire()
    cursor.execute(query)
    record=cursor.fetchone()
    lock.release()
    if record:
        lock.acquire()
        query="SELECT COURSE_INDEX FROM course WHERE COURSE='{}' and KISMODE='{}';".format(course_name, kis_mode)
        cursor.execute(query)
        result = cursor.fetchall()[0]
        result_json=json.dumps(result)
        result_pd=pd.read_json(StringIO(result_json))
        course_index=result_pd[0][0]
        lock.release()
        return course_index
    else:
        return 'error'
#course_index=find_course_index('design studies',2)

def generate_pie_chart(course_index):
    # check if employment data is available for the user-selected course info
    lock.acquire()
    cursor.execute("SELECT COURSE_INDEX FROM employment WHERE COURSE_INDEX=?",(str(course_index),))
    record = cursor.fetchone()
    lock.release()
    if record:
        # Select employment data (from employment sqlite table) associated to the 
        # given course index (i.e. to the user-selected course name and study mode)
        query="SELECT STUDY,UNEMP,PREVWORKSTUD,BOTH,NOAVAIL,WORK FROM employment WHERE COURSE_INDEX='{}';".format(course_index)
        lock.acquire()
        cursor.execute(query)
        result = cursor.fetchall()[0]
        result_json=json.dumps(result)
        result_df=pd.read_json(StringIO(result_json))
        lock.release()

        # Plot the pie chart
        labels=['Pursuing further studies','Unemployed','Worked AND/OR studied previously but not anymore','Both pursuing further studies AND working','Data not available','Working']
        fig = px.pie(result_df,values=0, names=labels,hole=0.4, color_discrete_sequence=px.colors.sequential.Burgyl,
                    title='WHAT ARE GRADUATES FROM YOUR COURSE DOING?')
        #format figure's layout
        fig.update_layout(
        title_font_family="Fantasy",
        title_font_size=25,
        title_font_color=px.colors.sequential.Burgyl[3],
        legend=dict(y=0.5),
        title=dict(x=0.5))
        return fig
    else:
        return 'error'
#generate_pie_chart(course_index)

def generate_satisfaction_indicators(course_index):
    # check if satisfaction data is available for the user-selected course info 
    lock.acquire()
    cursor.execute("SELECT COURSE_INDEX FROM satisfaction WHERE COURSE_INDEX=?",(str(course_index),))
    record = cursor.fetchone()
    lock.release()
    if record:
        #Select satisfaction data (from satisfaction sqlite table) associated to the 
        #given course index (i.e. to the user-selected course name and study mode)
        query="SELECT GOWORKMEAN,GOWORKONTRACK,GOWORKSKILLS FROM satisfaction WHERE COURSE_INDEX='{}';".format(course_index)
        lock.acquire()
        cursor.execute(query)
        result = cursor.fetchall()[0]
        result_json=json.dumps(result)
        result_df=pd.read_json(StringIO(result_json))
        lock.release()
        #Plot the indicators
        labels=['Agree or strongly agree that their current job is meaningful:',
                'Agree or strongly agree that their current job fits their future plan:',
                'Agree or strongly agree that they are using what they learnt in their studies in their current job:']
        fig = go.Figure()
        fig.add_trace(go.Indicator(
        value = result_df[0][0],
        title = {'text': str(labels[0]),'font_size':10},
        gauge = {'axis': {'range': [None, 100]},
                'bar': {'color': str(px.colors.sequential.Burgyl[0])}
                },
        number = {
            'suffix': "%"},
        domain = {'row': 0, 'column': 0, 'y': [0,0.2]}))
        
        fig.add_trace(go.Indicator(
        value = result_df[0][1],
        title = {'text': str(labels[1]),'font_size':10},
        gauge = {'axis': {'range': [None, 100]},
                'bar': {'color': str(px.colors.sequential.Burgyl[2])}
                },
        number = {
            'suffix': "%"},
        domain = {'row': 1, 'column': 0, 'y': [0.35,0.55]}))

        fig.add_trace(go.Indicator(
        value = result_df[0][2],
        title = {'text': str(labels[2]),'font_size':10},
        gauge = {'axis': {'range': [None, 100]},
                'bar': {'color': str(px.colors.sequential.Burgyl[4])}
                },
        number = {
            'suffix': "%"},
        domain = {'row': 2, 'column': 0, 'x': [0,0], 'y': [0.7,0.9]}))

        fig.update_layout(
        grid = {'rows': 3, 'columns': 1,'pattern':'independent'},
        template = {'data' : 
                    {'indicator': [{
                    'mode' : "number+gauge"}]
                    }
                    },
        title = {'text':'HOW DO GRADUATES FROM YOUR COURSE FEEL?',
                'x':0.5,
                'font':dict(size=25),
                'font_family': 'Fantasy',
                'font_color':px.colors.sequential.Burgyl[3]})
        return fig
    else:
        return 'error'

def generate_bar_chart(course_index, kis_level,countries=list):
    # check if salary data is available for the user-selected course info 
    if not countries:
        return 'no_countries_selected_error'
    lock.acquire()
    cursor.execute("SELECT COURSE_INDEX FROM salary WHERE COURSE_INDEX=?",(str(course_index),))
    record = cursor.fetchone()
    lock.release()
    if record:
        # Select salary data (from satisfaction sqlite table) associated to the 
        # given course index (i.e. to the user-selected course name and study mode)and kis_level
        country2cols={
            "UK":"GOSECLQ_UK,GOSECMED_UK,GOSECUQ_UK",
            "England":"GOSECLQ_E, GOSECMED_E, GOSECUQ_E",
            "Scotland":"GOSECLQ_S, GOSECMED_S, GOSECUQ_S",
            "Wales":"GOSECLQ_W, GOSECMED_W, GOSECUQ_W",
            "NI":"GOSECLQ_NI, GOSECMED_NI, GOSECUQ_NI",
        }
        #columns from database to select depending on user-enterred countries
        salary_cols=[]
        cnt=0
        for country in countries:
            if country in country2cols:
                salary_cols.append(country2cols[country])
                cnt+=1
            if cnt!=0 and cnt!=len(countries):
                salary_cols.append(',')
        
        #remove brackets 
        salary_cols=' '.join(salary_cols)
        # check if salary data is available for the user-selected course index (ie course name + study mode)+kis_level 
        lock.acquire()
        #cursor.execute("SELECT COURSE_INDEX FROM salary WHERE COURSE_INDEX=?",(str(course_index),))
        query="SELECT {} FROM salary WHERE COURSE_INDEX='{}' and KISLEVEL='{}' ;".format(salary_cols, course_index,kis_level)
        cursor.execute(query)
        record = cursor.fetchone()
        lock.release()
        if record:
            query="SELECT {} FROM salary WHERE COURSE_INDEX='{}' and KISLEVEL='{}' ;".format(salary_cols, course_index,kis_level)
            lock.acquire()
            cursor.execute(query)
            result = cursor.fetchall()[0]
            result_json=json.dumps(result)
            result_df=pd.read_json(StringIO(result_json))
            lock.release()
            #add a column to the dataframe with the countries names
            result_df['Country']=''
            start_idx=0
            for cnt in range(len(countries)):
                end_idx=start_idx+2
                result_df.loc[start_idx:end_idx,'Country']=countries[cnt]
                start_idx+=3

            #add a column to the dataframe with the salary type (lower quartile, median or upper quartile)
            result_df['Type']=''
            row=0
            for cnt in range(len(countries)):
                result_df.loc[row,'Type']='Lower Quartile'
                result_df.loc[row+1,'Type']='Median'
                result_df.loc[row+2,'Type']='Upper Quartile'
                row+=3

            # reformat the results dataframe so that it can be easily plotted (compatible with) using go.Bar
            reformatted_res_df=pd.DataFrame(columns=['Country', 'Lower Quartile', 'Median', 'Upper Quartile'])
            row_new_df=0
            for row_old_df in range(len(result_df)):
                reformatted_res_df.loc[row_new_df,'Country']=result_df.loc[row_old_df,'Country']
                if result_df.loc[row_old_df,'Type']=='Lower Quartile':
                    reformatted_res_df.loc[row_new_df,'Lower Quartile']=result_df.loc[row_old_df,0]

                elif result_df.loc[row_old_df,'Type']=='Median':
                    reformatted_res_df.loc[row_new_df,'Median']=result_df.loc[row_old_df,0]

                elif result_df.loc[row_old_df,'Type']=='Upper Quartile':
                    reformatted_res_df.loc[row_new_df,'Upper Quartile']=result_df.loc[row_old_df,0]
                
                if row_old_df==2 or row_old_df==5 or row_old_df==8 or row_old_df==11:
                    row_new_df+=1

            labels = countries
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=labels,
                y=reformatted_res_df['Lower Quartile'],
                name='Lower Quartile',
                marker_color=px.colors.sequential.Burgyl[0]
            ))
            fig.add_trace(go.Bar(
                x=countries,
                y=reformatted_res_df['Median'],
                name='Median',
                marker_color=px.colors.sequential.Burgyl[2]
            ))
            fig.add_trace(go.Bar(
            x=countries,
            y=reformatted_res_df['Upper Quartile'],
            name='Upper Quartile',
            marker_color=px.colors.sequential.Burgyl[4]
            ))
            # Here we modify the tickangle of the xaxis, resulting in rotated labels.
            fig.update_layout(title=dict(text='HOW MUCH ARE GRADUATES FROM YOUR COURSE PAID?',x=0.5), 
                            title_font_family="Fantasy",
                            title_font_color=px.colors.sequential.Burgyl[3],
                            title_font_size=25,
                            barmode='group', 
                            xaxis_tickangle=-45,
                            legend_font_size=15)
            return fig
        else:
            return 'error'
    else:
        return 'error'
    

# def info_tooltip_logo():
#     return html.Img(src=dash.get_asset_url("info_tooltip_logo.png"))