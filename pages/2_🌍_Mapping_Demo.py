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

import streamlit as st
import inspect
import textwrap
import pandas as pd
import pydeck as pdk
from utils import show_code
import plotly.express as px
import json
import plotly.graph_objects as go


from urllib.error import URLError


def mapping_demo():
    @st.experimental_memo
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )

    df = pd.read_csv('./data/Alfamart_di_makassar.csv')
    # df = pd.DataFrame(
    # np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    # columns=['lat', 'lon'])

    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/c/c4/Projet_bi%C3%A8re_logo_v2.png"

    icon_data = {
    # Icon from Wikimedia, used the Creative Commons Attribution-Share Alike 3.0
    # Unported, 2.5 Generic, 2.0 Generic and 1.0 Generic licenses
    "url": ICON_URL,
    "width": 242,
    "height": 242,
    "anchorY": 242,
    }

    df["icon_data"] = None
    for i in df.index:
        df["icon_data"][i] = icon_data

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=-5.1477,
            longitude=119.4327,
            zoom=11,
            pitch=50,
        ),
        layers=[
            # pdk.Layer(
            #     'HexagonLayer',
            #     data=df,
            #     get_position='[lon, lat]',
            #     radius=200,
            #     elevation_scale=4,
            #     elevation_range=[0, 1000],
            #     pickable=True,
            #     extruded=True,
            # ),
            pdk.Layer(
                'IconLayer',
                data=df,
                get_icon='icon_data',
                get_size=4,
                size_scale=15,
                get_position='[lng, lat]',
                pickable=True,
                # get_color='[200, 30, 0, 160]',
                # get_radius=200,
            ),
        ],
    ))

# @st.cache 
# def indo_map(data, geojson):
#     df1 = pd.read_csv(data).drop('Unnamed: 0', axis=1)
#     geojson_id = json.load(open(geojson))

#     fig3 = px.choropleth(df1, geojson=geojson_id, color="Rate",
#                         locations="Province", featureidkey="properties.NAME_1",
#     )
#     fig3.update_geos(fitbounds="locations", visible=False, bgcolor='#EEEEEE')
#     fig3.update_layout(title='Indonesia Poverty Rate', title_y=0.95, margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#EEEEEE',
#                         legend_orientation='h')
#     fig3.update_coloraxes(colorbar_orientation='h', colorbar_y=0.04, colorbar_len=0.5, colorbar_thickness=10)
#     fig3.update_traces(colorbar_orientation='h')
#     return fig3
    # st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})


st.set_page_config(page_title="Mapping Demo", page_icon="🌍")
st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
# st.write(
#     """This demo shows how to use
# [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
# to display geospatial data."""
# )

mapping_demo()
# st.plotly_chart(indo_map(data='data/data_chloropleth.csv', geojson='data/geo_IDN.json'), use_container_width=True, config={'displayModeBar': False})

# show_code(mapping_demo)
