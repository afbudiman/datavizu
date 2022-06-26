# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from turtle import title
import streamlit as st
# import inspect
# import textwrap
# import time
import numpy as np
# from utils import show_code
import plotly.express as px
import json
import plotly.graph_objects as go
from PIL import Image
import pandas as pd

def dashboard():
    # seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
    # stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')
     # Row A
    a1, a2, a3 = st.columns(3)
    a1.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
    a2.metric("Wind", "9 mph", "-8%")
    a3.metric("Humidity", "86%", "4%")

    # Row B
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Temperature", "70 °F", "1.2 °F")
    b2.metric("Wind", "9 mph", "-8%")
    b3.metric("Humidity", "86%", "4%")
    b4.metric("Humidity", "86%", "4%")

    # Row C
    # c1, c2 = st.columns((7,3))
    # with c1:
    #     st.markdown('### Heatmap')
    #     plost.time_hist(
    #     data=seattle_weather,
    #     date='date',
    #     x_unit='week',
    #     y_unit='day',
    #     color='temp_max',
    #     aggregate='median',
    #     legend=None)
    # with c2:
    #     st.markdown('### Bar chart')
    #     plost.donut_chart(
    #         data=stocks,
    #         theta='q2',
    #         color='company')

    # row D
    # d1, d2 = st.columns((3,7))

    # with d1:
    #     df = px.data.tips()
    #     fig = px.pie(df, values='tip', names='day')
    #     st.plotly_chart(fig, use_container_width=True)

    # with d2:
    df = px.data.stocks()
    fig = px.area(df, x='date', y="GOOG")
    fig.update_layout(title='Google Stock Market',
                      paper_bgcolor='#EEEEEE', 
                      plot_bgcolor='#EEEEEE', 
                      margin_pad=10,
                      margin_b=10,
                      margin_t=60,
                      height=300,
    )

    fig.update_xaxes(title='', gridcolor='#CACFD2')
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': False
    })


    c1, c2 = st.columns((7,3))
    with c1:
        fig1 = go.Figure(go.Bar(
                                x=[20, 14, 23, 45, 33, 27, 36],
                                y=['giraffes', 'orangutans', 'monkeys', 'crocodile', 'horse', 'tapir', 'nyamuk'],
                                orientation='h'))
        fig1.update_layout(title='Bar Chart Example', showlegend=False, height=300, margin={'t':60,'b':40,'l':20,'r':20}, 
                           plot_bgcolor='#EEEEEE', paper_bgcolor='#EEEEEE')
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
        values = [4500, 2500, 1053, 500]
        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.75)])
        fig2.update_layout(title='Pie Chart Example', title_y=0.5, title_x=0.5, showlegend=False, height=300, margin={'t':6,'b':6,'l':6,'r':6}, 
                           plot_bgcolor='#EEEEEE', paper_bgcolor='#EEEEEE')
        st.plotly_chart(fig2, use_container_width=True)


    d1, d2 = st.columns((5,5))
    with d1:
        z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
        fig4 = go.Figure(data=[go.Surface(z=z_data.values)])
        fig4.update_scenes(xaxis_showgrid=False, xaxis_backgroundcolor='#c8c8c8',
                           yaxis_showgrid=False, yaxis_backgroundcolor='#c8c8c8',
                           zaxis_showgrid=False, zaxis_backgroundcolor='#c8c8c8',
                          )
        fig4.update_layout(title='Mt Bruno Elevation', title_y=0.95, autosize=False,
                           width=500, height=400, paper_bgcolor='#EEEEEE',
                           margin=dict(l=60, r=40, b=45, t=40, pad=0))
        fig4.update_traces(showscale=False)
        st.plotly_chart(fig4, use_container_width=True, config={
            'displayModeBar': False
        })

    with d2:
        df = px.data.iris()
        fig5 = go.Figure(data=[go.Scatter3d(x=df['sepal_length'], y=df['sepal_width'], z=df['petal_width'], 
                                            mode='markers',
                                            marker=dict(
                                                size=4,
                                                color=df['species_id'],
                                                colorscale=['#187c9f', '#55189f', '#2a9f18'],
                                                opacity=0.8),
                                            )])
        fig5.update_scenes(xaxis_showgrid=False, xaxis_backgroundcolor='#c8c8c8',
                           yaxis_showgrid=False, yaxis_backgroundcolor='#c8c8c8',
                           zaxis_showgrid=False, zaxis_backgroundcolor='#c8c8c8',
                          )
        fig5.update_layout(title='3D Scatter Plot Example', title_y=0.95, autosize=False, paper_bgcolor='#EEEEEE',
                           width=500, height=400, margin=dict(l=60, r=40, b=45, t=40, pad=0))
        st.plotly_chart(fig5, use_container_width=True, config={
            'displayModeBar': False
        })


    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

    fig6 = go.Figure(data=go.Choropleth(
        locations = df['CODE'],
        z = df['GDP (BILLIONS)'],
        text = df['COUNTRY'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = 'GDP<br>Billions US$',
    ))

    fig6.update_layout(
        title_text='2014 Global GDP',
        title_y=0.94,
        paper_bgcolor='#EEEEEE',
        margin={"r":10,"t":50,"l":10,"b":10,"pad":0},
        geo=dict(
            bgcolor='#EEEEEE',
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                CIA World Factbook</a>',
            showarrow = False
        )]
    )
    st.plotly_chart(fig6, use_container_width=True, config={
        'displayModeBar': False
    })


    # df1 = pd.read_csv('data/data_chloropleth.csv').drop('Unnamed: 0', axis=1)
    # geojson_id = json.load(open('data/geo_IDN.json'))

    # fig3 = px.choropleth(df1, geojson=geojson_id, color="Rate",
    #                     locations="Province", featureidkey="properties.NAME_1",
    # )
    # fig3.update_geos(fitbounds="locations", visible=False, bgcolor='#EEEEEE')
    # fig3.update_layout(title='Indonesia Poverty Rate', title_y=0.95, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#EEEEEE',
    #                    legend_orientation='h')
    # fig3.update_coloraxes(colorbar_orientation='h', colorbar_y=0.04, colorbar_len=0.5, colorbar_thickness=10)
    # fig3.update_traces(colorbar_orientation='h')
    # st.plotly_chart(fig3, use_container_width=True, config={
    #     'displayModeBar': False
    # })


# def plotting_demo():
#     progress_bar = st.sidebar.progress(0)
#     status_text = st.sidebar.empty()
#     last_rows = np.random.randn(1, 1)
#     chart = st.line_chart(last_rows)

#     for i in range(1, 101):
#         new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#         status_text.text("%i%% Complete" % i)
#         chart.add_rows(new_rows)
#         progress_bar.progress(i)
#         last_rows = new_rows
#         time.sleep(0.05)

#     progress_bar.empty()

#     # Streamlit widgets automatically run the script from top to bottom. Since
#     # this button is not connected to any other logic, it just causes a plain
#     # rerun.
#     st.button("Re-run")


st.set_page_config(page_title="Dashboard Demo", page_icon="📈", layout="wide")

with open('style.css') as f:
  st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# st.markdown("# Plotting Demo")
# st.sidebar.header("Plotting Demo")
# st.write(
#     """This demo illustrates a combination of plotting and animation with
# Streamlit. We're generating a bunch of random numbers in a loop for around
# 5 seconds. Enjoy!"""
# )

dashboard()

# show_code(plotting_demo)
