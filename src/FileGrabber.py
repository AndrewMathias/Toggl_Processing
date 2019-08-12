# FileGrabber.py
# Author: Andrew Mathias
# Grabs entries from toggl.com using your API token

import requests
import base64
import datetime
from src.References import *


togglRequestURL = "https://toggl.com/reports/api/v2/details.csv"


string = myAPItoken+':api_token'

headers = {
    'Authorization':'Basic '+base64.b64encode(string.encode('ascii')).decode("utf-8")
}

# grabEntryList: returns a list of each time entry as a text line in chronological order
# beginning a numDays( a datetime.timedelta object) prior to the endDay(a datetime.(datetime/date) object) param
def grabEntryList(endDay, numDays):
    params = {
        'user_agent': email,

        'workspace_id': workspaceID,

        # date span of entries to be grabbed
        'since': str(endDay - numDays)[:10],
        'until': str(endDay)[:10]
    }

    responseFile = requests.get(togglRequestURL, headers = headers, params = params)
    entryList = responseFile.content.decode('iso-8859-1').split('\n')
    entryList = entryList[1:len(entryList) - 1]
    entryList.reverse()
    return entryList


