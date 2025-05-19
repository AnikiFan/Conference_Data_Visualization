import streamlit as st
import pandas as pd
import sys
import os
import streamlit.components.v1 as components
from lib import (
    conf_name_map,
    get_author_number_fig,
    get_author_number_data,
    get_graph_data, get_collaborate_graph
)

st.set_page_config(
    layout="wide",
    page_title="Collaboration🤝"
)
st.title("Collaboration🤝")

st.header("Authorship Distribution Across Conferences",divider="orange")
st.plotly_chart(get_author_number_fig())
st.divider()

st.header("Trends in Average Collaboration Size Across Conferences",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    options = st.multiselect(
        "Select conference to show",
        list(conf_name_map.values()),
        default=list(conf_name_map.values()),
        key="author_number_multiselectbox"
    )
with col1:
    st.line_chart(
        get_author_number_data().loc[lambda x: x.Conference.isin(options), :],
        x="Year",
        y="Average Number of Co-authors per Paper",
        color="Conference",
        height=800,
    )
st.divider()



st.header("Collaboration Flowmap of Research Institutions",divider="orange")
components.html(
    """
       <div style="text-align: center;"> 
            <iframe src="https://app.flowmap.city/public/943484c8-6887-41d7-a904-98298cb5bba7" width="100%" height="800" frameborder="0"></iframe>
       </div>
    """,
    scrolling=False,
    height=1200,
)
st.divider()

# Initialize
st.header("Collaboration Network of Research Institutions",divider="orange")
components.html(get_collaborate_graph(),height=1200)
st.divider()
