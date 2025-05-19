import streamlit as st
from lib import (
    get_available_fig,
    get_attribute_fig,
    conf_name_map,
    get_conf_time,
    get_conf_attribute_fig,
    get_sunburst_fig,
    get_count_data
)

st.set_page_config(
    layout="wide",
    page_title="Visualization Project",
    page_icon="🥳",
    initial_sidebar_state="expanded",
    menu_items={
        "About":"Made by Xiao Fan"
    }
)

st.title("Overview")

st.header("Available Conference Data",divider="orange")
st.plotly_chart(get_available_fig())
st.divider()

st.header("Attribute Availability Overview",divider="orange")
st.plotly_chart(get_attribute_fig())
st.divider()

st.header("Attribute Availability in Selected Conference and Time Range",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    select_conf = st.selectbox(
        "Select conference to show",
        list(conf_name_map.values()),
        key="conf_attribute_selectbox"
    )
    if get_conf_time().loc[select_conf, "min"] < get_conf_time().loc[select_conf,"max"]:
        begin_year, end_year = st.select_slider(
            "Select interval to show",
            options=range(get_conf_time().loc[select_conf, "min"],
                          get_conf_time().loc[select_conf,  "max"] + 1),
            value=(get_conf_time().loc[select_conf, "min"], get_conf_time().loc[select_conf,"max"]),
            key="conf_attribute_slider"
        )
    else:
        begin_year, end_year = get_conf_time().loc[select_conf, "min"], get_conf_time().loc[select_conf, "min"]
with col1:
    st.plotly_chart(get_conf_attribute_fig(select_conf, begin_year, end_year))
st.divider()

st.header("Proportion of Status Categories by Conference",divider="orange")
st.plotly_chart(get_sunburst_fig())
st.divider()



st.header("Annual Paper Counts by Conference",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    options = st.multiselect(
        "Select conference to show",
        list(conf_name_map.values()),
        default=list(conf_name_map.values()),
        key="count_multiselectbox"
    )
with col1:
    st.line_chart(
        get_count_data().loc[lambda x: x.Conference.isin(options), :],
        x="Year",
        y="Count",
        color="Conference",
        height=800,
    )

