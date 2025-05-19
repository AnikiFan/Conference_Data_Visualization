import streamlit as st
import pandas as pd
import sys
import os
from lib import (
    get_unique_meeting_fig,
    get_interval_fig,
    get_paper_count_fig,
    conf_name_map,
    get_paper_count_data, get_annual_paper_fig
)

st.set_page_config(
    layout="wide",
    page_title="Outcome🥳"
)
st.title("Outcome🥳")

st.header("Publication Output Over Academic Career Span",divider="orange")
st.plotly_chart(get_annual_paper_fig())
st.divider()

st.header("Conference Diversity Over Academic Career Span",divider="orange")
st.plotly_chart(get_unique_meeting_fig())
st.divider()


st.header("Time Gap Between First Publication and First First-Authorship Across Conferences",divider="orange")
st.plotly_chart(get_interval_fig())
st.divider()

st.header("Annual Publication Output by Scholar",divider="orange")
st.plotly_chart(get_paper_count_fig())
st.divider()

st.header("Trends in Per-Scholar Publication Rates Across Conferences",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    options = st.multiselect(
        "Select conference to show",
        list(conf_name_map.values()),
        default=list(conf_name_map.values()),
        key="paper_count_multiselectbox"
    )
with col1:
    st.line_chart(
        get_paper_count_data().loc[lambda x: x.meeting.isin(options), :].rename(
            columns={"meeting": "Conference", "count_": "Number of Paper", "year": "Year"}),
        x="Year",
        y="Number of Paper",
        color="Conference",
        height=800,
    )
st.divider()

