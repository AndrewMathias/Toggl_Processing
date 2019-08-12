# HelperFunctions.py
# Author: Andrew Mathias
# Various helper functions for processing data obtained from Toggl reports and graphing said data using plot.ly


from src.References import *
import datetime


# readTimerEntry
# @param entryLine: text line of a single timer entry
# @return: a string tuple (projects, description, startDate, startTime, endDate, endTime, duration, tags)
#          dates are in format YYYY-MM-DD and times are in HH:MM:SS 24-hour time
def readTimerEntry(entryLine):
    entryLine = adjustBeggnning(entryLine, gmail)
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


# Returns the entryLine param with the beginning adjusted to the first occurence of the target string
# If the target string does not appear in the entryLine, the orginial entryLine is returned
def adjustBeggnning(entryLine, target):
    if entryLine.find(target) != -1:
        return entryLine[entryLine.find(target) + len(target):]
    else:
        return entryLine


def getToken(entryLine):
    return entryLine[:entryLine.find(',')]


# Returns an int representing the numerical value of the day of the month
def dayNum(date):
    return int(date[8:10])


# Returns an int representing the numerical value of the month
def monthNum(date):
    return int(date[5:7])


# Returns an int representing the numerical value of the year
def yearNum(date):
    return int(date[:4])


# Returns an int representing the numerical value of the month that the majority of the week resides in given wednesday date
def whichMonthIsTheWeek(wednesday):
    return monthNum(wednesday)


#Returns the YYYY-MM-DD string for wednesday
def getWednesday(dayTokenLists):
    return str(dayTokenLists[3][0][ind["edI"]])


# Returns an int 1-4 representing the quarter the week resides in given the wednesday date of the week.
# The week is classified as belonging to the quarter in which the wednesday resides
def whichQuarter(wednesday):
    if whichMonthIsTheWeek(wednesday) <= 3:
        return 1
    elif whichMonthIsTheWeek(wednesday) <= 6:
        return 2
    elif whichMonthIsTheWeek(wednesday) <= 9:
        return 3
    else:
        return 4


# Returns a boolean whether this week is a different quarter than last week
def isNewQuarter(wednesday):
    thisWednesday = datetime.date(yearNum(wednesday), monthNum(wednesday), dayNum(wednesday))
    lastWednesday = thisWednesday - oneWeek
    return whichQuarter(str(thisWednesday)) != whichQuarter(str(lastWednesday))


# Returns the number of days between date and startDate given date is after startDate
# Accurate until the year 2400, which it will count as a leap year, if we still use the gregorian calendar that is
def relDayNum(date, startDate):
    if date[5:7] != startDate[5:7]:
        if startDate[5:7] == "04" or startDate[5:7] == "06" or startDate[5:7] == "09" or startDate[5:7] == "11":
            return dayNum(date) + 30 - dayNum(startDate)
        elif startDate[5:7] == "02":
            if isinstance(int(startDate[2:4]) / 4, int):
                return dayNum(date) + 29 - dayNum(startDate)
            else:
                return dayNum(date) + 28 - dayNum(startDate)
        else:
            return dayNum(date) + 31 - dayNum(startDate)
    else:
        return dayNum(date) - dayNum(startDate)


# Converts a 24-hour HH:MM:SS time into an integer of seconds
def timeToNum(time):
    return int(time[6:]) + (60 * int(time[3:5])) + (3600 * int(time[:2]))


# Converts an integer of seconds to 24-hour HH::MM::SS
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


# Converts an entryTuple back to the original string format provided by the Toggl report
def backToTimerEntry(entryTuple):
    if entryTuple == "Untracked":
        return entryTuple
    else:
        tags = entryTuple[ind["tagI"]]
        if tags.find(",") != -1:
            tags = '"' + tags + '"'
        return username + "," + email + ",," + entryTuple[ind["projI"]] + ",," + entryTuple[ind["descI"]] \
           + ",No," + entryTuple[ind["sdI"]] + "," + entryTuple[ind["stI"]] + "," + entryTuple[ind["edI"]] + "," \
           + entryTuple[ind["etI"]] + "," + entryTuple[ind["durI"]] + "," + tags + ","


# Returns an entryTuple which is the first entry for next week unless it was not tracked
def grabNextWeeksPortion(entryTuple):
    if entryTuple[ind["sdI"]] == entryTuple[ind["edI"]]:
        return "Untracked"
    else:
        return entryTuple[ind["projI"]], entryTuple[ind["descI"]], entryTuple[ind["edI"]], '00:00:00', entryTuple[ind["edI"]], \
           entryTuple[ind["etI"]], entryTuple[ind["etI"]], entryTuple[ind["tagI"]]


# Returns the entryTuple which is the last entry of the current week, edited to end before midnight if needed
def fixThisWeeksPortion(entryTuple):
    if entryTuple[ind["sdI"]] == entryTuple[ind["edI"]]:
        return entryTuple
    else:
        return entryTuple[ind["projI"]], entryTuple[ind["descI"]], entryTuple[ind["sdI"]], entryTuple[ind["stI"]], entryTuple[ind["sdI"]], "23:59:00", backToTime(timeToNum("23:59:00") - timeToNum(entryTuple[ind["stI"]])), entryTuple[ind["tagI"]]


def weekTuplesToString(weekTuple):
    return weekTuple[0] + ", " + weekTuple[1] + ", " + weekTuple[2] + ", "


# Returns a tuple of all the individual tags in the tags string
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


# Returns a dictionary of projects:colors(rgb) from the master dictionary of possible projects
def colorDictMaker(projectList):
    colorDict = {}
    for project in projectList:
        adjProject = removeChar(project, " ")
        adjProject = removeChar(adjProject, ".")
        colorDict[project] = masterColorsdict[adjProject]
    return colorDict


# Removes all instances of a char from the param str and returns the new str
def removeChar(str, char):
    while str.find(char) != -1:
        str = str[:str.find(char)] + str[str.find(char) + 1:]
    return str


# Returns a string of commas and the first letters of the tags up to 2 tags
def tagsInitials(tag):
    if tag == "":
        return "   "
    elif tag.find(',') == -1:
        return ", " + tag[:1]
    else:
        return ", " + tag[:1] + ", " + tag[tag.find(',') + 2: tag.find(',') + 3]


# Takes a 24-hr HH::MM::SS time and returns a new one rounded to the nearest minute
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


# Takes in an entryTuple and returns it with the times rounded to the nearest minute
def minuteResolutionEntry(entryTuple):
    return entryTuple[ind["projI"]], entryTuple[ind["descI"]], entryTuple[ind["sdI"]], \
           minuteResolutionTime(entryTuple[ind["stI"]]), entryTuple[ind["edI"]], \
           minuteResolutionTime(entryTuple[ind["etI"]]), entryTuple[ind["durI"]], entryTuple[ind["tagI"]]


# Reads a line from the weekly aggregate file and returns a 2-tuple of a 3-tuple (project, description, tags) and the value of seconds
def readWeeklyLineReport(line):
    tokenList = line.split(", ")
    tagIndex = 2
    tags = tokenList[tagIndex]
    while tagIndex < len(tokenList) - 2:
        tagIndex += 1
        tags += ", " + tokenList[tagIndex]
    return ((tokenList[0], tokenList[1], tags), timeToNum(tokenList[len(tokenList) - 1]))