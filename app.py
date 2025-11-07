# Import Libraries
import pandas as pd
import streamlit as st
from io import StringIO
from modules.utils import get_dir_path
from modules.graphs import getUrl, getEdges
from modules.charts import makeIcicle, makeSunburst, makeTreemap
from modules import formats, animated
import os
import plotly.graph_objects as go
import json
import streamlit.components.v1 as components


st.title('Hierarchical Data Viewer')

file_uploader=st.sidebar.file_uploader('Upload a csv file', type=['csv'])
file_io=None
dir_path=get_dir_path()

default_file=dir_path+"\data\employees.csv"
if file_uploader is not None:
    file_io=StringIO(file_uploader.getvalue().decode('utf-8'))
if file_io:
    df_orig=pd.read_csv(file_io).convert_dtypes()
else:
    df_orig=pd.read_csv(default_file)

df_cols=list(df_orig.columns)
#Select child and parent columns
with st.sidebar:
    with st.form('myform'):
        child=st.selectbox('Select Child Column',df_cols,index=0)
        parent=st.selectbox('Select Parent Column',df_cols, index=1)
        submitted = st.form_submit_button("Submit", width='content')
        df=df_orig[[child,parent]]
source, format, graph, chart, anim=st.tabs(['Source', 'Formats', 'Graph', 'Chart', 'Animated'])

# Show source dataframe
source.dataframe(df_orig)

# Display different format
with format:
    sel = st.selectbox(
        "Select a data format:",
        ["JSON", "XML", "YAML", "JSON Path", "JSON Tree"])

    root = formats.getJson(df)
    if sel == "JSON":
        jsn = json.dumps(root, indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "XML":
        xml = formats.getXml(root)
        st.code(xml, language="xml", line_numbers=True)
    elif sel == "YAML":
        yaml = formats.getYaml(root)
        st.code(yaml, language="yaml", line_numbers=True)
    elif sel == "JSON Path":
        jsn = json.dumps(formats.getPath(root, []), indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "JSON Tree":
        st.json(root)



# Display different charts
selection=chart.selectbox('Select a chart type',["treemap", "sunburst", "icicle"])

if selection=="treemap":
   fig=makeTreemap(df.iloc[:,0], df.iloc[:,1])
   chart.plotly_chart(fig, use_container_width=True, key='TreeMap')
elif selection=="sunburst":
   fig=makeSunburst(df.iloc[:,0], df.iloc[:,1])
   chart.plotly_chart(fig, use_container_width=True, key='Sunburst')
else:
   fig=makeIcicle(df.iloc[:,0], df.iloc[:,1])
   chart.plotly_chart(fig, use_container_width=True, key='Icicle')


# Display Graph
gh=getEdges(df)
graph.graphviz_chart(gh, use_container_width=True)
url=getUrl(gh)
graph.link_button("Visualize Online", url)
graph.code(gh)


# Display animation
with anim:
    sel = st.selectbox(
        "Select a D3 chart type:",
        ["Collapsible Tree", "Linear Dendrogram", "Radial Dendrogram", "Network Graph"])
    if sel == "Collapsible Tree":
        filename = animated.makeCollapsibleTree(df)
    elif sel == "Linear Dendrogram":
        filename = animated.makeLinearDendrogram(df)
    elif sel == "Radial Dendrogram":
        filename = animated.makeRadialDendrogram(df)
    elif sel == "Network Graph":
        filename = animated.makeNetworkGraph(df)

    with open(filename, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=2200, width=1000)


