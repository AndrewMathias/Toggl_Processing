# GanttMaker.py
# Author: Andrew Mathias
# Functions that facilitate the construction of plot.ly gantt charts given a list of entry tuples

from src.HelperFunctions import *
import plotly.figure_factory as ff


def ganttTimeFormat(date, time):
    return date + " " + minuteResolutionTime(time)


def ganttTuple(dataTuple):
    return (dataTuple[ind["descI"]] + tagsInitials(dataTuple[ind["tagI"]])), ganttTimeFormat(dataTuple[ind["sdI"]],
                                                                                             dataTuple[ind["stI"]]), \
           ganttTimeFormat(dataTuple[ind["edI"]], dataTuple[ind["etI"]]), dataTuple[ind["projI"]]


def ganttEntryDict(ganttTuple):
    return dict(Task=ganttTuple[0], Start=ganttTuple[1], Finish=ganttTuple[2], Resource=ganttTuple[3])


# Returns a gantt chart figure given the list of entries and the provided titles. Entries shorter than 5 minutes are ommitted
def makeGantt(entryTupleList, myTitle):
    df = []
    projectDict = {}
    for tuple in entryTupleList:
        projectDict[ganttTuple(tuple)[3]] = "True"
        if timeToNum(tuple[ind["durI"]]) >= 300:
            df.append(ganttEntryDict(ganttTuple(tuple)))

    colors = colorDictMaker(list(projectDict.keys()))

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', title=myTitle, show_colorbar=True, group_tasks=True)
    myMarker = dict(color = 'rgba(0, 0, 0, 0)')
    for i in fig['data']:
        i.update(marker=myMarker)
    return fig