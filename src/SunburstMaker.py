# GanttMaker.py
# Author: Andrew Mathias
# Functions that facilitate the construction of plot.ly sunburst charts given a dictionary of timer entries
# with the corresponding value of seconds

from HelperFunctions import *
import plotly.graph_objects as go


# Reduces a number of seconds into five minutes rounding down
def fiveMinuteRes(seconds):
    return int(seconds / 300)


# Returns a list of rgb colors corresponding with the list of labels
def colorsListSunburst(sunColorDict, justNameLabels):
    myColorList = []
    myColorList.append("")
    for label in justNameLabels:
        if label in sunColorDict:
            myColorList.append(sunColorDict[label])
        elif label == "Discouraged":
            myColorList.append("rgb(150, 20, 0)")
        elif label == "Encouraged":
            myColorList.append("rgb(0, 200, 140)")
        else:
            myColorList.append("")
    return myColorList


# Returns a figure of a sunburst chart given a dictionary of timers to value in seconds
def makeSunburst(timerDict, myTitle):
    myLabels = []
    justNameLabels = []
    myParents = []
    myValues = []
    myIDS = []
    projTimes = {}
    totalTime = 0

    # Filling projTimes
    for key in timerDict.keys():
        if key[0] in projTimes:
            projTimes[key[0]] += timerDict[key]
        else:
            projTimes[key[0]] = timerDict[key]

    # Summing total time
    for project in projTimes.keys():
        totalTime += projTimes[project]

    # Root sector
    myIDS.append(" ")
    myLabels.append(" ")
    myParents.append("")
    myValues.append(fiveMinuteRes(totalTime))

    # Adding branch and leaf sectors
    for key in timerDict.keys():
        # Project branches
        if key[0] + "<br>" + backToTime(projTimes[key[0]]) not in myLabels:
            myLabels.append(key[0] + "<br>" + backToTime(projTimes[key[0]]))
            myIDS.append(key[0] + "<br>" + backToTime(projTimes[key[0]]))
            justNameLabels.append(key[0])
            myParents.append(" ")
            myValues.append(fiveMinuteRes(projTimes[key[0]]))

        # Description branches/leaves
        myLabels.append(key[1] + "<br>" + backToTime(timerDict[key]))
        myIDS.append(key[1] + "<br>" + backToTime(timerDict[key]))
        justNameLabels.append(key[1])
        myParents.append(key[0] + "<br>" + backToTime(projTimes[key[0]]))
        myValues.append(fiveMinuteRes(timerDict[key]))

        # Tag leaves
        tags = separateTags(key[2])
        for tag in tags:
            if tag != '':
                myLabels.append(tag)
                myIDS.append(tag + key[0] + key[1])
                justNameLabels.append(tag)
                myParents.append(key[1] + "<br>" + backToTime(timerDict[key]))
                myValues.append(fiveMinuteRes(timerDict[key])/len(tags))


    trace = go.Sunburst(ids = myIDS, labels = myLabels, parents = myParents, values = myValues, branchvalues='total',
                       outsidetextfont = {"size": 20, "color": "#377eb8"}, leaf={"opacity":1},
                        marker = {"line": {"width": 2}, "colors": colorsListSunburst(colorDictMaker(list(projTimes.keys())), justNameLabels)})
    layout = go.Layout(
       margin=go.layout.Margin(t=0, l=0, r=0, b=0), title=go.layout.Title(
        text=myTitle, x=0.1, y=0.85)
    )

    fig = go.Figure([trace], layout)
    return fig