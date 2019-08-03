# FileGrabber.py
# Author: Andrew Mathias
# Grabs a weeks worth of entries from toggl.com using your API token

import requests
import base64
import datetime

oneWeek = datetime.timedelta(6)

togglRequestURL = "https://toggl.com/reports/api/v2/details.csv"
# TODO: add your api token here:
myAPItoken = "Yo insert your api token here"

string = myAPItoken+':api_token'

headers = {
    'Authorization':'Basic '+base64.b64encode(string.encode('ascii')).decode("utf-8")
}

# grabEntryList: returns a list of each time entry as a text line in chronological order
# beginning a week prior to the endDay param
def grabEntryList(endDay):
    params = {
        # TODO: add your email here:
        'user_agent': 'andrewsmathias2@gmail.com',
        # TODO: Add your workspace id here:
        'workspace_id': "2462605",
        # date span of entries to be grabbed
        # If you want to change the duration from a week you have to edit the timedelta object
        'since': str(endDay - oneWeek)[:10],
        'until': str(endDay)[:10]
    }

    responseFile = requests.get(togglRequestURL, headers = headers, params = params)
    entryList = responseFile.content.decode('iso-8859-1').split('\n')
    entryList = entryList[1:len(entryList) - 1]
    entryList.reverse()
    return entryList


