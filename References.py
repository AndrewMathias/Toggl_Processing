# References.py
# Author: Andrew Mathias
# Various reference variables for processing and graphing data from Toggl
import datetime

# files
weeklyAggregateFile = "C:/Users/andre/Documents/Time Tracking/Weekly_Time_Data_Aggregate.csv"
monthlyAggregateFile = "C:/Users/andre/Documents/Time Tracking/Monthly_Time_Data_Aggregate.csv"
weekReport = "ReportSourceFiles/Toggl_time_entries_2019-07-15_to_2019-07-21.csv"

# other references
oneDay = datetime.timedelta(1)
quotes = '"'
gmail = "@gmail.com"
ind = {"projI": 0, "descI": 1, "sdI": 2, "stI": 3, "edI": 4, "etI": 5, "durI": 6, "tagI": 7}
masterColorsdict = dict(Necessities = 'rgb(255, 204, 0)', Leisure = 'rgb(255, 204, 153)',
                        Work='rgb(0, 145, 0)', ProductiveMisc = 'rgb(255, 0, 0)',
                        PersonalProjects='rgb(0, 0, 187)', DesignTeams = 'rgb(244, 0, 255)',)
dayNumAbbrev = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}