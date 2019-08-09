# References.py
# Author: Andrew Mathias
# Various reference variables for processing and graphing data from Toggl

import datetime

# files
weeklyAggregateFile = "C:/Users/andre/Documents/Time Tracking/Weekly_Time_Data_Aggregate.csv"
quarterlyAggregateFile = "C:/Users/andre/Documents/Time Tracking/Quarterly_Time_Data_Aggregate.csv"
weekReport = "ReportSourceFiles/Toggl_time_entries_2019-07-08_to_2019-07-14 (3).csv"

# other references
oneDay = datetime.timedelta(1)
oneWeek = datetime.timedelta(7)
quotes = '"'
gmail = "@gmail.com"
ind = {"projI": 0, "descI": 1, "sdI": 2, "stI": 3, "edI": 4, "etI": 5, "durI": 6, "tagI": 7}
masterColorsdict = dict(Necessities = 'rgb(255, 204, 0)', Leisure = 'rgb(255, 204, 153)',
                        Work='rgb(0, 145, 0)', ProductiveMisc = 'rgb(255, 0, 0)',
                        PersonalProjects='rgb(0, 0, 187)', DesignTeams = 'rgb(244, 0, 255)',)
dayNumAbbrev = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}