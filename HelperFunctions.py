# HelperFunctions.py
# Author: Andrew Mathias
# Various helper functions for processing data obtained from Toggl reports and graphing said data using plot.ly
from References import *

# readTimerEntry
# @param entryLine: text line of a single timer entry
# @return: a string tuple (projects, description, startDate, startTime, endDate, endTime, duration, tags)
#          dates are in format YYYY-MM-DD and times are in HH:MM:SS 24-hour time
def readTimerEntry(entryLine):
    entryLine = adjustBeggnning(entryLine)
    entryLine = toNextComma(entryLine)
    entryLine = toNextComma(entryLine)

    project = getToken(entryLine)
    entryLine = toNextComma(entryLine)
    entryLine = toNextComma(entryLine)

    description = getToken(entryLine)
    entryLine = toNextComma(entryLine)
    entryLine = toNextComma(entryLine)

    startDate = getToken(entryLine)
    entryLine = toNextComma(entryLine)

    startTime = getToken(entryLine)
    entryLine = toNextComma(entryLine)

    endDate = getToken(entryLine)
    entryLine = toNextComma(entryLine)

    endTime = getToken(entryLine)
    entryLine = toNextComma(entryLine)

    duration = getToken(entryLine)
    entryLine = toNextComma(entryLine)

    if entryLine.find(quotes) != -1:
        entryLine = adjustBeggnning(entryLine, quotes)
        tags = entryLine[:entryLine.find(quotes)]
    else:
        tags = getToken(entryLine)

    return project, description, startDate, startTime, endDate, endTime, duration, tags


def toNextComma(entryLine):
    return adjustBeggnning(entryLine, ',')


def adjustBeggnning(entryLine, target):
    if entryLine.find(target) != -1:
        return entryLine[entryLine.find(target) + len(target):]
    else:
        return entryLine


def getToken(entryLine):
    return entryLine[:entryLine.find(',')]


def dayNum(date):
    date = date[date.find('-') + 1:]
    date = date[date.find('-') + 1:]
    return int(date)


def relDayNum(date, mon):
    if date[5:7] != mon[5:7]:
        if mon[5:7] == "04" or mon[5:7] == "06" or mon[5:7] == "09" or mon[5:7] == "11":
            return dayNum(date) + 30 - dayNum(mon)
        elif mon[5:7] == "02":
            if isinstance(int(mon[2:4]) / 4, int):
                return dayNum(date) + 29 - dayNum(mon)
            else:
                return dayNum(date) + 28 - dayNum(mon)
        else:
            return dayNum(date) + 30 - dayNum(mon)
    else:
        return dayNum(date) - dayNum(mon)


def timeToNum(time):
    return int(time[6:]) + (60 * int(time[3:5])) + (3600 * int(time[:2]))


def backToTime(time):
    seconds = time % 60
    minutes = (time // 60) % 60
    hours = time // 3600
    if hours < 10:
        hours = '0' + str(hours)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(hours) + ":" + str(minutes) + ":" + str(seconds)


def backToTimerEntry(dataTuple):
    if dataTuple == "Untracked":
        return dataTuple
    else:
        tags = dataTuple[ind["tagI"]]
        if tags.find(",") != -1:
            tags = '"' + tags + '"'
        return "Andrewsmathias42,andrewsmathias42@gmail.com,," + dataTuple[ind["projI"]] + ",," + dataTuple[ind["descI"]] \
           + ",No," + dataTuple[ind["sdI"]] + "," + dataTuple[ind["stI"]] + "," + dataTuple[ind["edI"]] + "," \
           + dataTuple[ind["etI"]] + "," + dataTuple[ind["durI"]] + "," + tags + ","


def grabNextWeeksPortion(dataTuple):
    if dataTuple[ind["sdI"]] == dataTuple[ind["edI"]]:
        return "Untracked"
    else:
        return dataTuple[ind["projI"]], dataTuple[ind["descI"]], dataTuple[ind["edI"]], '00:00:00', dataTuple[ind["edI"]], \
           dataTuple[ind["etI"]], dataTuple[ind["etI"]], dataTuple[ind["tagI"]]


def fixThisWeeksPortion(dataTuple):
    if dataTuple[ind["sdI"]] == dataTuple[ind["edI"]]:
        return dataTuple
    else:
        return dataTuple[ind["projI"]], dataTuple[ind["descI"]], dataTuple[ind["sdI"]], dataTuple[ind["stI"]], dataTuple[ind["sdI"]], "23:59:00", backToTime(timeToNum("23:59:00") - timeToNum(dataTuple[ind["stI"]])), dataTuple[ind["tagI"]]


def weekTuplesToString(weekTuple):
    return weekTuple[0] + ", " + weekTuple[1] + ", " + weekTuple[2] + ", "


def separateTags(tags):
    tagsList = []
    tags = adjustBeggnning(tags, '"')
    if tags.find(',') == -1:
        tagsList.append(tags)
    else:
        while tags.find(',') != -1:
            tagsList.append(tags[:tags.find(',')])
            tags = toNextComma(tags)
        tagsList.append(tags[:tags.find('"')])

    return tuple(tagsList)

def colorDictMaker(projectList):
    colorDict = {}
    for project in projectList:
        adjProject = removeChar(project, " ")
        adjProject = removeChar(adjProject, ".")
        colorDict[project] = masterColorsdict[adjProject]
    return colorDict

def minuteResolutionList(entryTokenList):
    newResList = []
    for entry in entryTokenList:
        newResList.append(minuteResolutionEntry(entry))
    return newResList


def removeChar(str, char):
    while str.find(char) != -1:
        str = str[:str.find(char)] + str[str.find(char) + 1:]
    return str


def tagsInitials(tag):
    if tag == "":
        return "   "
    elif tag.find(',') == -1:
        return ", " + tag[:1]
    else:
        return ", " + tag[:1] + ", " + tag[tag.find(',') + 2: tag.find(',') + 3]


def minuteResolutionTime (timeString):
    hours = timeString[:2]
    if int(timeString[6:]) < 30:
        return timeString[:6] + '00'
    else:
        minutes = timeString[3:5]
        minutes = int(minutes) + 1
        if minutes < 10:
            minutes = "0" + str(minutes)
        elif minutes >= 60:
            if minutes < 70:
                minutes = '0' + str(minutes - 60)
            else:
                minutes = str(minutes - 60)
            hours = int(hours) + 1
            if hours < 10:
                hours = '0' + str(hours)
            else:
                hours = str(hours)
        else:
            minutes = str(minutes)
        return hours + ":" + minutes + ":00"


def minuteResolutionEntry(dataTuple):
    return dataTuple[ind["projI"]], dataTuple[ind["descI"]], dataTuple[ind["sdI"]], \
           minuteResolutionTime(dataTuple[ind["stI"]]), dataTuple[ind["edI"]], \
           minuteResolutionTime(dataTuple[ind["etI"]]), dataTuple[ind["durI"]], dataTuple[ind["tagI"]]

