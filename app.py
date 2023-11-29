#!/usr/bin/env python
# coding: utf-8

# In[6]:


# 합본

import pandas as pd
from dash import Dash, dcc, html, Input, Output, State

import plotly.graph_objects as go
from plotly.subplots import make_subplots


df_cov = pd.read_csv('D:/disease_COVID19.csv')
df_cov


df_disease = pd.concat([pd.read_csv('D:/disease_ARI.csv'),
                        pd.read_csv('D:/disease_influenza.csv'),
                        pd.read_csv('D:/disease_SP.csv')])

#df_cov = pd.read_csv('D:/disease_COVID19.csv')

df_disease

# radioitems value
button = ['Acute Respiratory Infection', 'Influenza', 'Streptococcus Pneumoniae']

# App structure
app = Dash(__name__)
app.title = ('Dashboard | COVID-19 & Respiratory Disease Data')
server = app.server

# App layout
app.layout = html.Div([
    
    # Main Title
    html.H2('Impact of COVID-19 Pandamic on Occurence Trends of Resiratory Disease in Korea',
           style = {'textAlign': 'center'}
           ),
    
    # 탭 영역 설정
    dcc.Tabs([
        # tab 1
        dcc.Tab(label = 'Dashboard',
                style = {'padding': '3px', 'fontWeight': 'bold',
                         'borderBottom': '1px solid #d6d6d6'},
                selected_style = {'padding': '3px', 'backgroundColor': '#119DFF', 'color': 'white',
                                  'borderBottom': '1px solid #d6d6d6', 'borderTop': '1px solid #d6d6d6'},
                children = [
                   html.Div([
                       html.P(children = 'Disease Type: '),
                       dcc.RadioItems(id = 'radio',
                                      options = [{'label': i, 'value':i} for i in button],
                                      value = 'Acute Respiratory Infection',
                                      labelStyle = {'display': 'block'})
                   ]),
                   dcc.Graph(id = 'graph', 
                             style = {'width': '95%',
                                     'height': 650,
                                     'margin-left': 'auto',
                                     'margin-right': 0})
               ]),
        # tab 2
        dcc.Tab(label = 'Upload',
                style = {'padding': '3px', 'fontWeight': 'bold',
                         'borderBottom': '1px solid #d6d6d6'},
                selected_style = {'padding': '3px', 'backgroundColor': '#119DFF', 'color': 'white',
                                  'borderBottom': '1px solid #d6d6d6', 'borderTop': '1px solid #d6d6d6'},
                children = [
                    
                    html.Div([
                        html.Div([
                            dcc.Upload(id = 'up1',
                                       children = html.Div('Upload: COVID19'),
                                       style = {'width': '15%', 'height': '30px',
                                                'lineHeight': '30px', 'borderWidth': '1px',
                                                'borderStyle': 'dashed', 'borderRadius': '2px',
                                                'textAlign': 'center', 'float': 'left', 'display': 'inline-block'})
                        ]),
                        html.Div([
                            dcc.Upload(id = 'up2',
                                       children = html.Div('Upload: Disease'),
                                       style = {'width': '15%', 'height': '30px',
                                                'lineHeight': '30px', 'borderWidth': '1px',
                                                'borderStyle': 'dashed', 'borderRadius': '2px',
                                                'textAlign': 'center', 'float': 'left', 'display': 'inline-block'})
                        ])
                    ], style = {'width': '75%', 'overflow':'hidden'}), # hidden: 영역에 맞춰 나머지는 숨김처리
                    
                    dcc.Graph(id = 'auto', 
                              style = {'width': '95%', 
                                       'height': 650, 
                                       'margin-left': 'auto', 
                                       'margin-right':0})
                    # 그래프 높이를 layout에서 설정하기, callback에서 설정하면 tab 이동시 초기화됨
                ])
    ])
])

# Dashboard - graph Callback
@app.callback(Output('graph', 'figure'),
              Input('radio', 'value'))

def update_radio(val):
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs = [[{'secondary_y': True}]])
    
    # Bar Chart 1
    dis = df_cov['distance'].unique().tolist()
    col = ['#4088DA', '#89DEDF', '#FFB011', '#FC7001', '#E60000']
    
    # Loop - Distance
    for i in range(len(dis)):
        cov = df_cov[df_cov['distance'] == dis[i]]
        
        fig.add_trace(go.Bar(x = cov['week'],
                             y = cov['value'],
                             text = cov['distance'],
                             name = dis[i],
                             hovertemplate = '<b>2020</b><br>Week: %{x}<br>Distance: %{text}<br>Confirmed: %{y:,}',
                             hoverlabel_font_color = 'rgb(255,255,255)',
                             textposition = 'none',
                             marker_color = col[i]),
                      secondary_y = False)
        
    fig.update_layout(go.Layout(xaxis = dict(title = 'Time (week)',
                                             dtick = 1, tickangle = 0),
                                yaxis = dict(title = 'Cumulative Number of Confirmed Cases',
                                             tickformat = ',', showgrid = False),
                                legend = dict(orientation = 'h', 
                                              yanchor = 'top',
                                              y = 1.1,
                                              traceorder = 'normal')))

    # Line Chart
    yr = df_disease['year'].unique().tolist()
    line = ['dash', 'dot', 'solid']
    
    for i in range(len(yr)):
        df = df_disease[(df_disease['disease'] == val) & (df_disease['year'] == yr[i])]
        
        fig.add_trace(go.Scatter(x = df['week'],
                                 y = df['value'],
                                 text = df['year'],
                                 name = yr[i],
                                 hovertemplate = '<b>%{text}</b><br>Week: %{x}<br>Patient: %{y:,}',
                                 mode = 'lines',
                                 line = {'dash': line[i], 'color':'black', 'width': 1}),
                      secondary_y = True)
    
    # 보조축 title
    fig.update_yaxes(title_text = 'Number of Case(' + val + ')', tickformat = ',', secondary_y = True)
    
    return fig

import io
import base64

# 데이터 업로드시 파일이름이 base64로 인코딩되므로 이를 디코딩하는 함수 설정
def process_content(contents):
    type, data = contents.split(',')
    decoded = base64.b64decode(data)
    return decoded

# Upload - Graph Callback
@app.callback(Output('auto', 'figure'),
              [Input('up1', 'contents'), Input('up2', 'contents')])

def update_files(content1, content2):
    
    # create figure with secondary y-axis
    fig = make_subplots(specs = [[{'secondary_y': True}]])
    
    # upload data 처리
    data1 = process_content(content1)
    up_cov = pd.read_csv(io.StringIO(data1.decode('utf-8'))) # io.StringIO: 문자열을 파일형식으로 변경
    
    # settings
    dis = up_cov['distance'].unique().tolist()
    col = ['#4088DA', '#89DEDF', '#FFB011', '#FC7001', '#E60000']
    
    # Loop - Distance
    for i in range(len(dis)):
        cov = up_cov[up_cov['distance'] == dis[i]]
        
        fig.add_trace(go.Bar(x = cov['week'],
                             y = cov['value'],
                             text = cov['distance'],
                             name = dis[i],
                             hovertemplate = '<b>2020</b><br>Week: %{x}<br>Distance: %{text}<br>Confirmed: %{y:,}',
                             hoverlabel_font_color = 'rgb(255,255,255)',
                             textposition = 'none',
                             marker_color = col[i]),
                      secondary_y = False)
        
    fig.update_layout(go.Layout(xaxis = dict(title = 'Time (week)',
                                             dtick = 1, tickangle = 0),
                                yaxis = dict(title = 'Cumulative Number of Confirmed Cases',
                                             tickformat = ',', showgrid = False),
                                legend = dict(orientation = 'h', 
                                              yanchor = 'top',
                                              y = 1.1,
                                              traceorder = 'normal')))
    
    if content2 != None:
        # upload data 처리 - 호흡기 질환 데이터
        data2 = process_content(content2)
        up_dis = pd.read_csv(io.StringIO(data2.decode('utf-8')))
        
        # Line Chart
        yr = up_dis['year'].unique().tolist()
        dis_nm = up_dis['disease'].unique().tolist()[0]
        line = ['dash', 'dot', 'solid']

        for i in range(len(yr)):
            df = up_dis[(up_dis['year'] == yr[i])]

            fig.add_trace(go.Scatter(x = df['week'],
                                     y = df['value'],
                                     text = df['year'],
                                     name = yr[i],
                                     hovertemplate = '<b>%{text}</b><br>Week: %{x}<br>Patient: %{y:,}',
                                     mode = 'lines',
                                     line = {'dash': line[i], 'color':'black', 'width': 1}),
                          secondary_y = True)

        # 보조축 title
        fig.update_yaxes(title_text = 'Number of Case(' + dis_nm + ')', tickformat = ',', secondary_y = True)

    return fig



# In[8]:


# Run App
if __name__ == '__main__':
    app.run_server(debug = False, port=8055)


# In[2]:


get_ipython().system(' pip install gunicorn')


# In[4]:


get_ipython().system(' pip freeze')

get_ipython().system(' conda list')

