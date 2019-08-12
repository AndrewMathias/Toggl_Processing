# References.py
# Author: Andrew Mathias
# Various reference variables for processing and graphing data from Toggl

import datetime

# boolean flag options

# weekStartsMon: Only matters with the titles and file names of the charts
# True: assuming you run the script on Monday. Charts will be labeled Mon-Sun with Monday being the oldest data
# False: assuming you run the script on Sunday. Charts will be labeled Sun-Sat with Sunday being the oldest data
weekStartsMon = False

# removeGanttDotsButAlsoLegend:
# True: removes weird white dots on the edges of bars in Gantt charts but also makes the colors in the legend invisible
removeGanttDotsButAlsoLegend = True

# recordWeeklySummary:
# True: records a summary of each timer and the time spent in the weekly aggregate file
# False: only records the straddled record in the weekly aggregate file
recordWeeklySummary = True

# recordQuarterlySummary: Cannot be printed or even calculated unless recordWeeklySummary is set to True
# True: records a similar summary to the weekly summary but for 3 months
# I may add functionality to be able to make a quarterly sunburst chart in the future
# This is likely to run into issues if recordWeeklySummary is ever turned false for any number of weeks spanning a quarter
recordQuarterlySummary = True

# createGanttCharts:
# True: creates pdf Gantt(schedule/timeline like bar charts) charts for every day in the past week
createGanttCharts = True

# createSunburstCharts:
# True: creates pdf Sunburst charts (multi-level pie charts) for every day in the past week
createSunburstCharts = True

# createFullWeekSunburstChart:
# True: creates a single sunburst chart breaking down how your time was spent over the whole week
createFullWeekSunburstChart = True

# files
# TODO: Add path for weekly Aggregate file and cross-week record communication in these quotes:
weeklyAggregateFile = ""

# TODO: Add path for quarterly Aggregate file in these quotes:
quarterlyAggregateFile = ""

# TODO: Add path for folder to hold all your charts in these quotes:
trackedTimeDataFolderPath = ""

# only for processing data from manually downloaded csv detailed reports.
weekReport = "Put path to .csv file here"

# personal info

# TODO: Put your Toggl username in these quotes:
username = ""

# TODO: Put your Toggl email address in these quotes:
email = ""

# TODO: Put your Toggl API token in these quotes:
myAPItoken = ""

# TODO: Put your Toggl workspace ID in these quotes:
# You can find your workspace ID by going to the reports section of the Toggl website.
# Your worskspace ID is the number in the URL
workspaceID = ""

# Color configuration:

# Fill this in with all your possible projects and the associated rgb colors you want.
# Remove all spaces and periods from the project names. Mine are left in as examples

masterColorsdict = dict(Necessities = 'rgb(255, 204, 0)', Leisure = 'rgb(255, 204, 153)',
                        Work='rgb(0, 145, 0)', ProductiveMisc = 'rgb(255, 0, 0)',
                        PersonalProjects='rgb(0, 0, 187)', DesignTeams = 'rgb(244, 0, 255)',)

# Fill this with your tags and the associated rgb colors you want. Mine are left in as examples
# If you want the tag segments on the sunburst chart to be the same color as the project which it is tagging,
# simply make these empty curly braces
tagColorsdict = {"Encouraged": "rgb(0, 200, 140)", "Discouraged": "rgb(150, 20, 0)"}

# other references
oneDay = datetime.timedelta(1)
oneWeek = datetime.timedelta(7)
oneWeekSpan = datetime.timedelta(6)
quotes = '"'
gmail = "@gmail.com"
ind = {"projI": 0, "descI": 1, "sdI": 2, "stI": 3, "edI": 4, "etI": 5, "durI": 6, "tagI": 7}
dayNumAbbrevSun = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
dayNumAbbrevMon = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}