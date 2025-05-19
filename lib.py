import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from d3graph import d3graph,vec2adjmat

conf_type_map = {
    'CVPR': 'CV',
    'ICCV': 'CV',
    'ECCV': 'CV',
    'WACV': 'CV',
    'SIGGRAPH': 'CV',
    'SIGGRAPH Asia': 'CV',

    'ACL': 'NLP',
    'EMNLP': 'NLP',
    'CoLM': 'NLP',

    'NeurIPS': 'ML',
    'ICML': 'ML',
    'ICLR': 'ML',
    'AISTATS': 'ML',

    'AAAI': 'AI',
    'IJCAI': 'AI',

    'The Web Conference': 'Others',
    'ACM MM': 'Others',
    'CoRL': 'Others'
}
conf_name_map = {
    'cvpr': 'CVPR',
    'colm': 'CoLM',
    'acmmm': 'ACM MM',
    'www': 'The Web Conference',
    'icml': 'ICML',
    'acl': 'ACL',
    'corl': 'CoRL',
    'nips': 'NeurIPS',
    'siggraphasia': 'SIGGRAPH Asia',
    'ijcai': 'IJCAI',
    'wacv': 'WACV',
    'iccv': 'ICCV',
    'iclr': 'ICLR',
    'eccv': 'ECCV',
    'aaai': 'AAAI',
    'aistats': 'AISTATS',
    'siggraph': 'SIGGRAPH',
    'emnlp': 'EMNLP'
}
reverse_conf_name_map = {
    val:key for key, val in conf_name_map.items()
}


@st.cache_data(persist="disk",show_spinner=True)
def read_data():
    raw = pd.read_csv("data/raw.csv").replace(conf_name_map)
    return raw

@st.cache_data(persist="disk",show_spinner=True)
def read_numeric_data():
    raw = pd.read_csv("data/numeric_raw.csv").replace(conf_name_map)
    return raw

@st.cache_data(persist="disk",show_spinner=True)
def read_available():
    raw = pd.read_csv("data/available.csv", index_col=0)
    return raw


@st.cache_data(persist="disk",show_spinner=True)
def get_conf_time():
    if not os.path.exists("./data/conf_time_data.csv"):
        (
            read_data()
            .loc[:, ["year", "meeting"]]
            .groupby("meeting")
            .agg(["min", "max"])
            .reset_index()
            .replace(conf_name_map)
            .set_index("meeting")
            .pipe(lambda x: x.set_axis(x.columns.get_level_values(1), axis=1))
            .to_csv("./data/conf_time_data.csv")
        )
    return pd.read_csv("./data/conf_time_data.csv",index_col=0)


@st.cache_data(persist="disk",show_spinner=True)
def get_sunburst_data():
    if not os.path.exists("./data/sunburst_data.csv"):
        (
            pd
            .DataFrame(read_data().loc[:, ["meeting", "status"]].value_counts())
            .reset_index()
            .rename(columns={0: "count"})
            .replace(conf_name_map)
            .to_csv("./data/sunburst_data.csv",index=False)
        )
    return pd.read_csv("./data/sunburst_data.csv",)


@st.cache_data(persist="disk",show_spinner=True)
def get_count_data():
    if not os.path.exists("./data/count_data.csv"):
        (
            read_data()
            .loc[:, ["meeting", "year"]]
            .value_counts()
            .reset_index()
            .rename(columns={0: "count"})
            .replace(conf_name_map)
            .assign(year=lambda x: x.year.astype(str))
            .rename(columns={"meeting": "Conference", "year": "Year", "count": "Count"})
            .to_csv("./data/count_data.csv",index=False)
        )
    return pd.read_csv("./data/count_data.csv")


@st.cache_data(persist="disk",show_spinner=True)
def get_sunburst_fig():
    fig = px.sunburst(
        get_sunburst_data(),
        path=["meeting", "status"],
        values="count",
        template="plotly_dark"
    )
    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=800,
        width=800
    )
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_available_fig():
    data = read_available()

    fig = go.Figure()

    # 添加热图主体
    fig.add_trace(go.Heatmap(
        z=data,
        x=[str(x) for x in data.columns],
        y=data.index,
        colorscale=[
            [0.0, "black"],  # 0 -> black (Not Available)
            [0.00001, "white"],  # >0 -> white (Available)
            [1.0, "white"]
        ],
        showscale=False
    ))

    # 添加图例说明用的“假点”
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, color="black"),
        name="Not Available"
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="markers",
        marker=dict(size=10, color="white", line=dict(width=1, color="gray")),
        name="Available"
    ))

    # 更新布局
    fig.update_layout(
        width=1200,
        height=800,
        legend=dict(
            title=None,
            orientation="v",  # 垂直排列
            x=1.0,  # 靠右边缘
            xanchor="right",
            y=-0.2,  # 底部
            yanchor="bottom",
            bgcolor="rgba(0,0,0,0)",  # 背景透明（可选）
            font=dict(color="white")  # 白色文字配合 dark 主题
        )
    )

    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_attribute_data():
    if not os.path.exists("./data/attribute_data.csv"):
        (
            read_data()
            .notna()
            .assign(meeting=raw.meeting)
            .groupby("meeting")
            .mean()
            .rename(index=conf_name_map)
            .rename_axis("Attribute", axis="columns")
            .rename_axis("Conference", axis="index")
            .to_csv("./data/attribute_data.csv",index=False)
        )
    return pd.read_csv("./data/attribute_data.csv")


@st.cache_data(persist="disk",show_spinner=True)
def get_attribute_fig():
    fig = px.imshow(
        get_attribute_data(),
        color_continuous_scale=[
            [0.0, "black"],
            [1.0, "white"]
        ],
        aspect="auto",
        template="plotly_dark"
    )
    fig.update_traces(zmin=0)
    fig.update_xaxes(tickangle=45)
    fig.update_coloraxes(
        colorbar=dict(
            title="Availability",
            tickformat=".0%",  # 显示为百分比，例如 0.75 → 75%
            ticks="outside"
        )
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_conf_attribute_data(conf, start, end):
    return (
            read_numeric_data()
            .loc[lambda df:(df.meeting == conf) & (df.year.between(start, end)), :]
            .sort_values(by="year")
            .reset_index(drop=True)
            .dropna(axis=1, how="all")
            .apply(lambda row: row.mask(row.notna(), int(row.year)), axis=1)
            .apply(lambda row: row.mask(lambda x: x != row.year, np.inf), axis=1)
            .T
        )


@st.cache_data(persist="disk",show_spinner=True)
def get_conf_attribute_fig(conf, start, end):
    fig = px.imshow(get_conf_attribute_data(conf, start, end), template="plotly_dark")
    fig.update_coloraxes(
        colorbar=dict(
            title="Available Data",
            ticks="outside"
        )
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_corr_data(conf, options):
    return read_numeric_data().loc[lambda x: x.meeting == conf, options].corr()


@st.cache_data(persist="disk",show_spinner=True)
def get_corr_fig(conf, options):
    fig = px.imshow(get_corr_data(conf, options), template="plotly_dark")
    fig.update_coloraxes(
        cmin=0,  # 最小值为 0
        cmax=1,  # 最大值为 1
        colorbar=dict(
            title="Correlation",  # 色条标题
            ticks="outside"
        )
    )
    fig.update_layout(
        width=800,
        height=800
    )
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_violin_data(conf, attribute, begin_year, end_year):
    return (
            read_numeric_data()
            .loc[
                lambda x: (x.meeting == conf) & (x.year.between(begin_year, end_year)) & (x.status.notna()),
                ["status","title"] + [attribute]
            ]
            .rename(columns={"status":"Status","title":"Title"})
        )


@st.cache_data(persist="disk",show_spinner=True)
def get_violin_fig(conf, attribute, begin_year, end_year):
    fig = px.violin(
        get_violin_data(conf, attribute, begin_year, end_year).rename(columns={attribute: f"Value of {attribute}"}),
        x="Status",
        y=f"Value of {attribute}",
        color="Status",
        hover_data="Title",
        box=True,
        points="outliers",
        template="plotly_dark"
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    for trace in fig.data:
        if trace.type == 'violin':  # 只改散点部分
            trace.jitter = 0.5
            trace.marker.size = 4
            trace.pointpos = 0  # 点在箱线中线位置附近抖动
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_unique_meeting_fig():
    fig = px.violin(
        pd
        .read_csv("./data/first_author_info.csv")
        .groupby(["elapsed", "author"])
        .meeting_unique_count_upto_elapsed
        .unique()
        .explode()
        .reset_index()
        .assign(elapsed=lambda x: x.elapsed.astype(str))
        .replace(conf_name_map)
        .rename(columns={"elapsed": "Years Since First Publication",
                         "meeting_unique_count_upto_elapsed": "Number of Distinct Conferences Published In",
                         "author": "Author"}),
        x='Years Since First Publication',  # x轴：离散变量（建议是有限个值）
        y='Number of Distinct Conferences Published In',  # y轴：数值型变量
        points="outliers",  # 显示所有数据点
        hover_data=['Author'],  # 鼠标悬停显示作者
        box=True,  # 显示箱线
        template='plotly_dark',
        color="Years Since First Publication",
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    for trace in fig.data:
        if trace.type == 'violin':  # 只改散点部分
            trace.jitter = 0.5
            trace.marker.size = 4
            trace.pointpos = 0  # 点在箱线中线位置附近抖动
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_annual_paper_fig():
    fig = px.violin(
        pd
        .read_csv("./data/first_author_info.csv")
        .groupby(["author", "elapsed"])
        .apply(lambda x: len(x))
        .reset_index()
        .rename(columns={0: "Annual Paper Count", "author": "Author", "elapsed": "Years Since First Publication"}),
        x='Years Since First Publication',  # x轴：离散变量（建议是有限个值）
        y='Annual Paper Count',  # y轴：数值型变量
        points="outliers",  # 显示所有数据点
        hover_data=['Author'],  # 鼠标悬停显示作者
        box=True,  # 显示箱线
        template='plotly_dark',
        color="Years Since First Publication"
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    for trace in fig.data:
        if trace.type == 'violin':  # 只改散点部分
            trace.jitter = 0.5
            trace.marker.size = 4
            trace.pointpos = 0  # 点在箱线中线位置附近抖动
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_paper_count_fig():
    fig = px.violin(
        pd
        .read_csv("./data/first_author_info.csv")
        .groupby(["year", "author"])
        .paper_count
        .unique()
        .explode()
        .reset_index()
        .assign(year=lambda x: x.year.astype(str))
        .replace(conf_name_map)
        .rename(columns={"year": "Year","paper_count":"Annual Paper Count", "author": "Author"}),
        x='Year',  # x轴：离散变量（建议是有限个值）
        y='Annual Paper Count',  # y轴：数值型变量
        points="outliers",  # 显示所有数据点
        hover_data=['Author'],  # 鼠标悬停显示作者
        box=True,  # 显示箱线
        template='plotly_dark',
        color="Year"
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    for trace in fig.data:
        if trace.type == 'violin':  # 只改散点部分
            trace.jitter = 0.5
            trace.marker.size = 4
            trace.pointpos = 0  # 点在箱线中线位置附近抖动
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_interval_fig():
    fig = px.violin(
        pd
        .read_csv("./data/author_info.csv")
        .groupby(["meeting", "author"])
        .interval
        .unique()
        .explode()
        .reset_index()
        .replace(conf_name_map)
        .rename(columns={"meeting": "Conference",
                         "interval": "Years Between First Publication and First First-Author Paper",
                         "author": "Author"}),
        x='Conference',  # x轴：离散变量（建议是有限个值）
        y='Years Between First Publication and First First-Author Paper',  # y轴：数值型变量
        points=False,  # 显示所有数据点
        hover_data=['Author'],  # 鼠标悬停显示作者
        box=True,  # 显示箱线
        template='plotly_dark',
        color="Conference"
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_author_number_fig():
    if not os.path.exists("./data/author_number.csv"):
        (
            read_data()
            .assign(author_number=lambda x: x.author.map(lambda s: len(
                sum([ss.split(';') for ss in (s.split(',') if not isinstance(s, float) else [])], []))))
            .replace(conf_name_map)
            .rename(columns={"meeting": "Conference", "title": "Title","author_number":"Number of Authors per Paper"})
            .loc[:,["Conference","Title","Number of Authors per Paper"]]
            .to_csv("./data/author_number.csv",index=False)
        )

    fig = px.violin(
        pd.read_csv("./data/author_number.csv"),
        x='Conference',  # x轴：离散变量（建议是有限个值）
        y='Number of Authors per Paper',  # y轴：数值型变量
        points="outliers",  # 显示所有数据点
        hover_data=['Title'],  # 鼠标悬停显示作者
        box=True,  # 显示箱线
        template='plotly_dark',
        color="Conference"
    )
    fig.update_layout(
        width=1200,
        height=800
    )
    for trace in fig.data:
        if trace.type == 'violin':  # 只改散点部分
            trace.jitter = 0.5
            trace.marker.size = 4
            trace.pointpos = 0  # 点在
    return fig


@st.cache_data(persist="disk",show_spinner=True)
def get_author_number_data():
    if not os.path.exists("./data/author_number_data.csv"):
        (
            read_data()
            .assign(author_number=lambda x: x.author.map(
                lambda s: len(sum([ss.split(';') for ss in (s.split(',') if not isinstance(s, float) else [])], []))))
            .loc[lambda x: x.author_number > 0, :]
            .groupby(["meeting", "year"])
            .author_number
            .mean()
            .reset_index()
            .replace(conf_name_map)
            .rename(columns={"meeting": "Conference", "author_number": "Average Number of Co-authors per Paper","year": "Year"})
            .loc[:,["Conference","Average Number of Co-authors per Paper","Year"]]
            .to_csv("./data/author_number_data.csv",index=False)
        )
    return pd.read_csv("./data/author_number_data.csv")


@st.cache_data(persist="disk",show_spinner=True)
def get_paper_count_data():
    return (
        pd
        .read_csv("./data/first_author_info.csv")
        .assign(count_=lambda x: x.groupby(["year", "author", "meeting"]).paper_count.transform("count"))
        .groupby(["year", "meeting"])
        .count_
        .mean()
        .reset_index()
        .replace(conf_name_map)
    )

@st.cache_data(persist="disk",show_spinner=True)
def get_graph_data():
    return (pd.read_csv("./data/adjmat_greater_than_50.csv"),pd.read_csv("./data/node_info.csv",index_col=0))

@st.cache_data(persist="disk",show_spinner=True)
def get_collaborate_graph():
    if not os.path.exists("./data/graph.html"):
        vec, node_info = get_graph_data()
        D3 = d3graph()
        adjmat = vec2adjmat(vec.source, vec.target, vec.weight)
        D3.graph(adjmat=adjmat, size=node_info.loc[adjmat.index, "count"].tolist())
        D3.set_edge_properties(directed=True, marker_end='arrow')
        with open("./data/graph.html","w") as f:
            f.write(D3.show(filepath=None))
    with open("./data/graph.html","r") as f:
        return f.read()