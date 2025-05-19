import streamlit as st
import pandas as pd
import sys
import os
import re
from glob import glob
from lib import (
    conf_name_map,
    reverse_conf_name_map
)
import os

st.set_page_config(
    layout="wide",
    page_title="Topic🤯"
)
st.title("Topic🤯")

st.header("Keyword Trends in Conference Papers Over the Years",divider="orange")
col1, col2 = st.columns([4, 1])
with col2:
    select_conf = st.selectbox(
        "Select a conference to show",
        conf_name_map.values(),
        key="wordcloud_selectbox"
    )
with col1:
    years = [
        int(re.search(r'\d{4}', fig).group())
        for fig
        in glob(os.path.join(os.curdir, "data", "wordcloud", f"*{reverse_conf_name_map[select_conf]}*"))
    ]
    years.sort()

    if len(years) >1:
        year = st.select_slider(
            "Select a year to show",
            options = years
        )
    else:
        year = years[0]
        st.text(f"Displaying wordcloud of {years[0]}")
    st.image(os.path.join(os.curdir,"data","wordcloud",f"{reverse_conf_name_map[select_conf]}_{year}.png"))

st.divider()

