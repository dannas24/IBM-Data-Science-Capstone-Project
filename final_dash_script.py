#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# In[2]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"


# In[3]:


spacex_df = pd.read_csv(url).drop(columns="Unnamed: 0")


# In[4]:


max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# In[5]:


# Create a dash application
app = dash.Dash(__name__)


# In[6]:


dropdown_options = [
    {'label': 'ALL', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
]


# In[7]:


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    value="ALL",
                                    options=dropdown_options,
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                ),
                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={int(num): str(int(num)) for num in np.linspace(start=0, stop=9600, num=5, endpoint=True)},
                                    value=[min_payload, max_payload]
                                ),
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# In[8]:


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches By Sites',
            hole=0.3
        )

    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site].copy()
        filtered_df["Success"] = filtered_df["class"].apply(lambda x: "Success" if x == 1 else "Failure")
        fig = px.pie(
            filtered_df,
            names='Success',
            title=f'Total Success Launches for site {entered_site}',
            hole=0.3
        )

    fig.update_layout(
    title={
        "font": {"size": 23},
        "x": 0.5  # Centers the title
    })


    return fig


# In[9]:


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='payload-slider', component_property='value'), Input(component_id='site-dropdown', component_property='value')])

def update_input_container(payload_range, entered_site):

    min_val, max_val = payload_range

    filtered_df = spacex_df[spacex_df["Payload Mass (kg)"].between(min_val, max_val)].copy()

    title = "Correlation between Payload and Success for all Sites"

    if entered_site != "ALL":

        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site].copy()

        title = "Correlation between Payload and Success for Site {}".format(entered_site)


    fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=title
    )

    fig.update_yaxes(
    tickvals=[0, 1],
    ticktext=["Failure", "Success"],
)

    fig.update_layout(
    title= {
        "font": {"size": 23},
        "x": 0.5  # Centers the title
    })

    return fig


# In[10]:

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Important: must be 0.0.0.0, not localhost
        port=8050,  # Use Railway's PORT
        debug=False
    )

