import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
from st_aggrid import AgGrid
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

@st.experimental_memo(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    rows = [dict(row) for row in rows_raw]
    return rows

st.title("Analyzing Chicago Crime Data")
st.markdown('''The dataset can be found [here](https://console.cloud.google.com/bigquery?project=our-metric-297306&ws=!1m5!1m4!4m3!1sbigquery-public-data!2schicago_crime!3scrime)
''')

st.subheader('How the data looks like')
df = run_query("SELECT * FROM `bigquery-public-data.chicago_crime.crime` LIMIT 1000")
df = pd.DataFrame(df)
AgGrid(df, editable=True)

st.subheader('Number of crimes 2001-2022')
df1a = run_query('''select year, count(year) as total from `bigquery-public-data.chicago_crime.crime`
                   group by year 
                   order by year
                   ''')
df1a = pd.DataFrame(df1a)

fig1a = px.area(df1a, x="year", y="total")
st.plotly_chart(fig1a, use_container_width=True)

st.subheader('Number of crimes 2001-2022 per month')
df1b = run_query('''select FORMAT_DATE("%Y-%m", date) as year_month, count(unique_key) as total 
                    from `bigquery-public-data.chicago_crime.crime`
                    group by year_month 
                    order by year_month
                   ''')
df1b = pd.DataFrame(df1b)

fig1b = px.area(df1b, x="year_month", y="total")
st.plotly_chart(fig1b, use_container_width=True)

st.subheader('Number of crimes in each type of crime')
df2 = run_query('''select primary_type, count(primary_type) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by primary_type
                   order by total desc
                   ''')
df2 = pd.DataFrame(df2)                   

fig2 = px.bar(df2[:10], x="total", y="primary_type", orientation='h')
fig2.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Number of theft in each detail desctription")
df2a = run_query('''select primary_type, description, count(description) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   where primary_type = 'THEFT'
                   group by primary_type, description
                   order by total desc
                   ''')
df2a = pd.DataFrame(df2a)  

fig2a = px.bar(df2a[:10], x="total", y="description", orientation='h')
fig2a.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig2a, use_container_width=True)


st.subheader('The trend of three top different crime categories')
df2b = run_query('''select primary_type, FORMAT_DATE("%Y-%m", date) as year_month, count(unique_key) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   where primary_type in ('THEFT', 'BATTERY', 'CRIMINAL DAMAGE')
                   group by primary_type, year_month
                   order by primary_type, year_month
                   ''')
df2b = pd.DataFrame(df2b)                   

fig2b = px.line(df2b, x="year_month", y="total", color='primary_type')
fig2b.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig2b, use_container_width=True)

st.subheader('Top crime description in each crime categories')
df2c = run_query('''select tt.* 
                   from (select primary_type, description, count(description) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by primary_type, description) tt
                   inner join 
                            (select primary_type, max(total) as total
                            from (select primary_type, description, count(description) as total
                            from `bigquery-public-data.chicago_crime.crime`
                            group by primary_type, description)
                            group by primary_type) groupedtt 
                   ON tt.primary_type = groupedtt.primary_type
                   AND tt.total = groupedtt.total
                   order by primary_type
                   
                   ''')
df2c = pd.DataFrame(df2c).iloc[:,:3]     
st.dataframe(df2c, width=478)              

st.subheader('Number of crimes in different locations')
df3 = run_query('''select location_description, count(location_description) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by location_description
                   order by total desc
                   ''')
df3 = pd.DataFrame(df3)                   

fig3 = px.bar(df3[:10], x="total", y="location_description", orientation='h')
fig3.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3, use_container_width=True)

st.subheader('Number of crimes in different categories occurred in street')
df3a = run_query('''select location_description, primary_type, count(primary_type) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by location_description, primary_type
                   order by total desc
                   ''')
df3a = pd.DataFrame(df3a)                   

fig3a = px.bar(df3a[:10], x="total", y="primary_type", orientation='h')
fig3a.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3a, use_container_width=True)

st.subheader('Number of crimes occurred in different blocks')
df3b = run_query('''select block, count(block) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by block
                   order by total desc
                   ''')
df3b = pd.DataFrame(df3b)                   

fig3b = px.bar(df3b[:10], x="total", y="block", orientation='h')
fig3b.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig3b, use_container_width=True)

st.subheader('Comparison of arrested and not arrested crimes')
df4 = run_query('''select arrest, count(arrest) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by arrest
                   order by arrest desc
                   ''')
df4 = pd.DataFrame(df4)                   

fig4 = px.pie(df4, values="total", names="arrest", hole=.6)
st.plotly_chart(fig4, use_container_width=True)

st.subheader('What crimes categories resulted in arrest and not')
df4a = run_query('''select arrest, primary_type, count(primary_type) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by arrest, primary_type
                   order by arrest desc
                   ''')
df4a = pd.DataFrame(df4a)                   

fig4a = px.sunburst(df4a, path=['arrest', 'primary_type'], values='total', color='primary_type')
st.plotly_chart(fig4a, use_container_width=True)

st.subheader('Comparison of domestic violance and non domestic violance crimes')
df5 = run_query('''select domestic, count(domestic) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by domestic
                   order by total desc
                   ''')
df5 = pd.DataFrame(df5)                   

fig5 = px.pie(df5, values="total", names="domestic", hole=.6)
st.plotly_chart(fig5, use_container_width=True)

st.subheader('What crime categories included in domestic violance and non domestic violance crime')
df5a = run_query('''select domestic, primary_type, count(primary_type) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   group by domestic, primary_type
                   order by domestic desc
                   ''')
df5a = pd.DataFrame(df5a)                   

fig5a = px.sunburst(df5a, path=['domestic', 'primary_type'], values='total', color='primary_type')
st.plotly_chart(fig5a, use_container_width=True)

st.subheader('Number of crimes based on district')
df7 = run_query('''select district, count(district) as total
                   from `bigquery-public-data.chicago_crime.crime`
                   where district is not null
                   group by district
                   order by total desc
                   ''')
df7 = pd.DataFrame(df7)         
df7a = pd.DataFrame({'district':range(1,99)})
df7b = pd.merge(df7a, df7, how="left", on=["district"]).fillna(0)   

with urlopen('https://raw.githubusercontent.com/blackmad/neighborhoods/master/chicago.geojson') as response:
    counties = json.load(response)

fig7 = px.choropleth_mapbox(df7b, geojson=counties, color="total",
                    locations="district", featureidkey="properties.cartodb_id",
                    mapbox_style="carto-positron", zoom=9, center = {"lat": 41.8381, "lon": -87.6298}, opacity=0.5
                   )

fig7.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig7, use_container_width=True)