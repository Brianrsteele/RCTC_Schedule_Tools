# RCTC_Schedule_Tools
Python tools to assist with scheduling courses at Rochester Community and Technical College, in Rochester, MN.

## scheduleToCSV_regex.py
To use this script, download a schedule from [https://secure.rctc.edu/apps/course_schedule/draft/](https://secure.rctc.edu/apps/course_schedule/draft/), open the file, and save the file as a text document. Pass the name of the text document as an argument at the command line, i.e. "python scheduleToCSV_reges.py the_schedule.txt". The script was written for Python 3.7.

## timeTable.py
This script will generate a one week time table visually representing courses, based on a passed CSV file. Pass a file name for the CSV file as an argument at the command line, i.e. "python timeTable.py example_file.csv". The script will generate an SVG file with the time table. The script will look for a css stylesheet named "styles.css" so that colors can be customized.
