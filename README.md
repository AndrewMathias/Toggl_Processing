# Toggl_Processing 

## Overview

This repo uses Toggl's API to grab time traking data and graph it using Gantt and Sunburst charts from the plot.ly library. It is intended to be run the same day every week.

## Requirements:

First off, you'll need some way to edit and run a Python script.

These packages need to be downloaded before running the script:

* Easy to install using pip:
    * plotly
    * numpy
    * psutil
    * requests
    
* Orca: different methods of installation found here: https://github.com/plotly/orca

## Setup:

* Fill in the References.py file (located in the src folder) with the necessary information 

* You're ready to start running the script. I recommend running it the same day every week. If you're on Windows, you can make a batch file and automatically run it every week through the task scheduler.