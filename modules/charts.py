import pandas as pd
import plotly.graph_objects as go

def makeTreemap(labels, parents):
    data=go.Treemap(ids=labels,labels=labels, parents=parents, root_color="lightgrey")
    figure=go.Figure(data=data)
    return figure

def makeSunburst(labels, parents):
    data=go.Sunburst(ids=labels,labels=labels, parents=parents, root_color="lightgrey")
    figure=go.Figure(data=data)
    return figure

def makeIcicle(labels, parents):
    data=go.Icicle(ids=labels,labels=labels, parents=parents, root_color="lightgrey")
    figure=go.Figure(data=data)
    return figure