#!/usr/bin/python

import os
import datetime
from HelperFunctions import *
from References import *
from SunburstMaker import makeSunburst
from GanttMaker import makeGantt
from FileGrabber import grabEntryList


###Local File Test
# weekData = open(weekReport)
# entryList = list(weekData)
# entryList = entryList[1:]

###FileGrabber
date = datetime.datetime.today() - oneDay #Auto runs every Sunday 11:30 AM. Gives report of Sunday - Saturday
entryList = grabEntryList(date)

## entryList now contains each timer entry line as each element of the list

entryTupleList = []

### Obtain entry that straddled the previous week
weeklyData = open(weeklyAggregateFile)
line = ""
for line in weeklyData:
    pass
lastWeeksEntry = readTimerEntry(line)
if lastWeeksEntry != "Untracked":
    entryTupleList.append(lastWeeksEntry)
weeklyData.close()


### Adding new entries and fixing final entry
for i in entryList:
    entryTupleList.append(readTimerEntry(i))

straddledRecordToWrite = backToTimerEntry(grabNextWeeksPortion(entryTupleList[len(entryTupleList) - 1]))
entryTupleList[len(entryTupleList) - 1] = fixThisWeeksPortion(entryTupleList[len(entryTupleList) - 1])

## entryToken list now contains a list of tuples which in turn contain the pertinent information
## to be used by the graphing portion of the script
##
## Example reference of a duration: entryTupleList[0][ind["durI"]]


startDay = entryTupleList[0][ind["sdI"]]

### Processing and Consolidating Data

## Lists for the entryTuples corresponding to each day
mT = []
tT = []
wT = []
rT = []
fT = []
aT = []
uT = []
dayTokenLists = [mT, tT, wT, rT, fT, aT, uT]

## Sorting entryTuples into lists for each day for Gantt charts
for entry in entryTupleList:
    if entry[ind["sdI"]] != entry[ind["edI"]]:
        dayTokenLists[relDayNum(entry[ind["sdI"]], startDay)].append(fixThisWeeksPortion(entry))
        dayTokenLists[relDayNum(entry[ind["edI"]], startDay)].append(grabNextWeeksPortion(entry))
    else:
        dayTokenLists[relDayNum(entry[ind["sdI"]], startDay)].append(entry)


## Dictionaries to hold timers to time spent for each day
M = {}
T = {}
W = {}
R = {}
F = {}
A = {}
U = {}
cumulativeDayTimes = [M, T, W, R, F, A, U]

## Accumulating time for each timer in the respective day dictionary
for entry in entryTupleList:
    if (entry[ind["projI"]], entry[ind["descI"]], entry[ind["tagI"]]) in \
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay)]:
        if entry[ind["sdI"]] == entry[ind["edI"]]:
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay)][(entry[ind["projI"]], entry[ind["descI"]],
                                                                entry[ind["tagI"]])] += timeToNum(entry[ind["durI"]])
        else:
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay)][(entry[ind["projI"]], entry[ind["descI"]],
                                                                    entry[ind["tagI"]])] += timeToNum("24:00:00") - \
                                                                                            timeToNum(entry[ind["stI"]])
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay) + 1][(entry[ind["projI"]], entry[ind["descI"]],
                                                                    entry[ind["tagI"]])] = timeToNum(entry[ind["etI"]])
    else:
        if entry[ind["sdI"]] == entry[ind["edI"]]:
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay)][(entry[ind["projI"]], entry[ind["descI"]],
                                                                entry[ind["tagI"]])] = timeToNum(entry[ind["durI"]])
        else:
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay)][(entry[ind["projI"]], entry[ind["descI"]],
                                                                    entry[ind["tagI"]])] = timeToNum("24:00:00") - \
                                                                                            timeToNum(entry[ind["stI"]])
            cumulativeDayTimes[relDayNum(entry[ind["sdI"]], startDay) + 1][(entry[ind["projI"]], entry[ind["descI"]],
                                                                    entry[ind["tagI"]])] = timeToNum(entry[ind["etI"]])
## cumulativeDayTimes now contains 7 dictionaries for Mon-Sun which each contain the keys (project, description, tags)
## and the value of time in seconds


## Accumulating timer total times for the week
cumulativeWeekTimes = {}
for day in cumulativeDayTimes:
    for entry in day.keys():
        if entry in cumulativeWeekTimes:
            cumulativeWeekTimes[entry] += day[entry]
        else:
            cumulativeWeekTimes[entry] = day[entry]

## cumulativeWeekTimes is a dictionary with the keys (project, description, tags) and the value of time in seconds


### Printing to weekly aggregate file

weeklyData = open(weeklyAggregateFile, 'a')
weeklyData.write("\n\nWeek " + entryTupleList[0][ind["sdI"]] + " : " + entryTupleList[len(entryTupleList) - 1][ind["edI"]]
                 + "\n")
## Print week's information
for timer in cumulativeWeekTimes.keys():
    weeklyData.write(weekTuplesToString(timer) + backToTime(cumulativeWeekTimes[timer]) + "\n")
weeklyData.write("\n" + straddledRecordToWrite)
weeklyData.close()

### Creating chart files

## Creating week folder
dirName = "C:/Users/andre/Documents/Time Tracking/" + entryTupleList[0][ind["sdI"]] + " to " + entryTupleList[len(entryTupleList) - 1][ind["edI"]]
if not os.path.exists(dirName):
    os.mkdir(dirName)

## Gantt charts
dayCount = 0
for day in dayTokenLists:
    ganttFig = makeGantt(day, dayNumAbbrev[dayCount])
    ganttFig.write_image("../../../Documents/Time Tracking/" + entryTupleList[0][ind["sdI"]] + " to " + entryTupleList[len(entryTupleList) - 1][ind["edI"]] + "/" + dayNumAbbrev[dayCount] + " Gantt.pdf")
    dayCount += 1

## Daily Sunburst charts
dayCount = 0
for day in cumulativeDayTimes:
    sunFig = makeSunburst(day, dayNumAbbrev[dayCount])
    sunFig.write_image("../../../Documents/Time Tracking/" + entryTupleList[0][ind["sdI"]] + " to " + entryTupleList[len(entryTupleList) - 1][ind["edI"]] + "/" + dayNumAbbrev[dayCount] + " Sunburst.pdf")
    dayCount += 1

## Weekly Sunburst chart
sunFig = makeSunburst(cumulativeWeekTimes, "Full Week")
sunFig.write_image("../../../Documents/Time Tracking/" + entryTupleList[0][ind["sdI"]] + " to " + entryTupleList[len(entryTupleList) - 1][ind["edI"]] + "/" + "Week Sunburst.pdf")

# TODO: 1. Clean up and comment SunburstMaker and GanttMaker
# TODO: 2. Create quarterly recording

# TODO: Maybe add descriptive file names w/ dates
