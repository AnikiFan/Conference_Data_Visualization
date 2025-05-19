import streamlit as st
from lib import (
    conf_name_map,
    get_conf_time,
    read_numeric_data,
    get_violin_fig,
    get_corr_fig
)

st.set_page_config(
    layout="wide",
    page_title="Research🥸"
)
st.title("Research🥸")

st.header("Correlation Matrix of Paper Attributes",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    select_conf = st.selectbox(
        "Select a conference to show",
        conf_name_map.values(),
        key="corr_selectbox"
    )
    options = st.multiselect(
        "Select attributes to calculate",
        read_numeric_data().select_dtypes(include="number").columns,
        default=["gs_citation", "rating_avg", "confidence_avg", "replies_avg", "authors#_avg", "correctness_avg",
                 "presentation_avg", "recommendation_avg", "technical_novelty_avg", "empirical_novelty_avg",
                 "soundness_avg", "contribution_avg"]
    )
with col1:
    st.plotly_chart(get_corr_fig(select_conf, options))
st.divider()

st.header("Distribution of Selected Metric by Paper Status",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    select_conf = st.selectbox(
        "Select a conference to show",
        conf_name_map.values(),
        key="violin_selectbox"
    )

    if get_conf_time().loc[select_conf, "min"] < get_conf_time().loc[select_conf,  "max"]:
        begin_year, end_year = st.select_slider(
            "Select interval to show",
            options=range(get_conf_time().loc[select_conf, "min"],
                          get_conf_time().loc[select_conf, "max"] + 1),
            value=(
                get_conf_time().loc[select_conf, "min"], get_conf_time().loc[select_conf,  "max"]),
            key="violin_slider"
        )
    else:
        begin_year, end_year = get_conf_time().loc[select_conf, "min"], get_conf_time().loc[
            select_conf, "min"]
    option = st.selectbox(
        "Select an attribute to compare",
        read_numeric_data().select_dtypes(include="number").dropna(how="all", axis=1).columns,
        key="violin_multiselectbox"
    )
with col1:
    st.plotly_chart(get_violin_fig(select_conf, option, begin_year, end_year))

st.divider()

