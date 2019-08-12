#TimeChartCreator.py
# Author: Andrew Mathias
# Grabs data from Toggl, processes it, and produces pdf graphs of last week's tracked data

#!/usr/bin/python

import os
from src.HelperFunctions import *
from src.References import *
from src.SunburstMaker import makeSunburst
from src.GanttMaker import makeGantt
from src.FileGrabber import grabEntryList

if weekStartsMon:
    dayNumAbbrev = dayNumAbbrevMon
else:
    dayNumAbbrev = dayNumAbbrevSun


# ###Local File Test - grabs data from a manually saved detailed report (csv format) instead of the Toggl API
# weekData = open(weekReport)
# entryList = list(weekData)
# entryList = entryList[1:]

###FileGrabber
date = datetime.datetime.today() - oneDay
entryList = grabEntryList(date, oneWeekSpan)


## entryList now contains each timer entry line as each element of the list

entryTupleList = []

### Obtain entry that straddled the previous week
weeklyAggregateFileSetUp = True
if not os.path.exists(weeklyAggregateFile):
    weeklyAggregateFileSetUp = False
else:
    weeklyData = open(weeklyAggregateFile, "r")
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
dayTokenLists = [uT, mT, tT, wT, rT, fT, aT]

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
cumulativeDayTimes = [U, M, T, W, R, F, A]

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


### Printing to weekly and quarterly aggregate files
if weeklyAggregateFileSetUp:
    weeklyData = open(weeklyAggregateFile, 'a')
else:
    weeklyData = open(weeklyAggregateFile, 'w+')
    weeklyData.write(str(yearNum(getWednesday(dayTokenLists))) + "-Q" + str(whichQuarter(getWednesday(dayTokenLists))))

if recordWeeklySummary:
    ## Print quarter information
    if recordQuarterlySummary:
        if isNewQuarter(getWednesday(dayTokenLists)):
            weeklyData.write("\n\n" + str(yearNum(getWednesday(dayTokenLists))) + "-Q" + str(whichQuarter(getWednesday(dayTokenLists))))
            weeklyData.close()
            weeklyData = open(weeklyAggregateFile, 'r')
            lastQuarter = str(yearNum(getWednesday(dayTokenLists) - oneWeek)) + "-Q" + str(whichQuarter(getWednesday(dayTokenLists)-oneWeek))

            ## Accumulate data from weeklyAggregateFile
            cumulativeQuarterTimes = {}
            recordFlag = False
            for line in weeklyData:
                if recordFlag:
                    if line.find(',') != -1:
                        if getToken(line) != username:
                            entry = readWeeklyLineReport(line)
                            if entry[0] in cumulativeQuarterTimes:
                                cumulativeQuarterTimes[entry[0]] += entry[1]
                            else:
                                cumulativeQuarterTimes[entry[0]] = entry[1]

                elif line[:2] == "20":
                    if line[:7] == lastQuarter:
                        recordFlag = True

            # write quarterly data
            quarterlyData = open(quarterlyAggregateFile, 'a+')
            quarterlyData.write(yearNum(getWednesday(dayTokenLists)) + "-Q" + str(whichQuarter(getWednesday(dayTokenLists))) + "\n\n")
            for timer in cumulativeQuarterTimes.keys():
                quarterlyData.write(weekTuplesToString(timer) + backToTime(cumulativeQuarterTimes[timer]) + "\n")
            quarterlyData.write("\n\n")

            weeklyData = open(weeklyAggregateFile, 'a')

    weeklyData.write("\n\nWeek " + entryTupleList[0][ind["sdI"]] + " : " + entryTupleList[len(entryTupleList) - 1][ind["edI"]]
                     + "\n\n")
    ## Print week's information
    for timer in cumulativeWeekTimes.keys():
        weeklyData.write(weekTuplesToString(timer) + backToTime(cumulativeWeekTimes[timer]) + "\n")
weeklyData.write("\n" + straddledRecordToWrite)
weeklyData.close()

### Creating chart files

## Creating week folder
dirName = trackedTimeDataFolderPath + getWednesday(dayTokenLists)[:4] + "/Q" + \
          str(whichQuarter(getWednesday(dayTokenLists))) + "/" + entryTupleList[0][ind["sdI"]] + \
          " to " + entryTupleList[len(entryTupleList) - 1][ind["edI"]]
if not os.path.exists(dirName):
    os.mkdir(dirName)

## Gantt charts
if createGanttCharts:
    dayCount = 0
    for day in dayTokenLists:
        ganttFig = makeGantt(day, dayNumAbbrev[dayCount])
        daySeparation = datetime.timedelta(7 - dayCount)
        ganttFig.write_image(dirName + "/" + str(datetime.datetime.today() - daySeparation)[5:10] + " " +
                             dayNumAbbrev[dayCount] + " Gantt.pdf")
        dayCount += 1

## Daily Sunburst charts
if createSunburstCharts:
    dayCount = 0
    for day in cumulativeDayTimes:
        sunFig = makeSunburst(day, dayNumAbbrev[dayCount])
        daySeparation = datetime.timedelta(7 - dayCount)
        sunFig.write_image(dirName + "/" + str(datetime.datetime.today() - daySeparation)[5:10] + " " +
                           dayNumAbbrev[dayCount] + " Sunburst.pdf")
        dayCount += 1

## Weekly Sunburst chart
if createFullWeekSunburstChart:
    sunFig = makeSunburst(cumulativeWeekTimes, "Full Week")
    sunFig.write_image(dirName + "/" + "Week Sunburst.pdf")

