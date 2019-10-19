# RCTC_Schedule_Tools
Python tools to assist with scheduling courses at Rochester Community and Technical College, in Rochester, MN.

## scheduleToCSV_regex.py
To use this script, download a schedule from [https://secure.rctc.edu/apps/course_schedule/draft/](https://secure.rctc.edu/apps/course_schedule/draft/), open the file, and save the file as a text document. Pass the name of the text document as an argument at the command line, i.e. "python scheduleToCSV_reges.py the_schedule.txt". The script was written for Python 3.7.

## timeTable.py
This script will generate a one week time table visually representing courses, based on a passed CSV file. Pass a file name for the CSV file as an argument at the command line, i.e. "python timeTable.py example_file.csv". The script will generate an SVG file with the time table. The script will look for a css stylesheet named "styles.css" so that colors can be customized.

## SPRING_2020_RCTC_ART.py
This script will download enrollment and other course information from Minnstate departments by scraping the public schedule page at [https://eservices.minnstate.edu/registration/search/basic.html?campusid=306&searchrcid=0306&searchcampusid=306](https://eservices.minnstate.edu/registration/search/basic.html?campusid=306&searchrcid=0306&searchcampusid=306). 

* The script was written for Python 3.6
* The script requires the requests and bs4 modules, which need to be imported using pip.
* The file "RCTC_FINE_ART_search.csv holds school codes and department names for Minnstate Schools and departments at those schools. There is a list of school codes for Minnstate schools in the python script, if you want to expand or change the search. Note that department names are not the same at other Minnstate schools.
