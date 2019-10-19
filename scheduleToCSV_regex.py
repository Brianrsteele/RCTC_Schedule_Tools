#! /usr/bin/python3

"""
scheduleToCSV.py by Brian Steele
9/15/2018

This script with assist with turning schedule documents sent to PL/DCs into CSV files that 
can be analyzed using excel or sharepoint lists.

1. Open the .dot file with the blue squares that was downloaded from sharepoint.
2. Save it as a plain text file, text encoding = "Mac OS (Default)" and End lines with "CR only"
3. Put a copy of this script and the plain text file in the same folder
4. Makre sure SCHEDULE_TEXT_FILE = the name of the text file
5. This will output to the file name in SCHEDULE_TEXT_OUTPUT_FILE
6. Open a blank excel document and choose "File/Import" and select the CSV option, tab delimited

"""

import csv
import re
import sys


SCHEDULE_TEXT_FILE = sys.argv[1]
SCHEDULE_TEXT_OUTPUT_FILE = sys.argv[1][:-4] + ".csv"
print(SCHEDULE_TEXT_OUTPUT_FILE)


schedule_file = open(SCHEDULE_TEXT_FILE)
schedule_file_contents = schedule_file.read()
schedule_file.close()

course_entry = re.compile(r"(\d{6})\n(\w*)\n(\d{4})\n(\d{2})\n([\S+' ']+)\n(\d+)\n(\w)\n([MTWHF' ']*)\n(ARR|[\d]*:[\d]*\s\w{2})\n(ARR|[\d]*:[\d]*\s\w{2})\n(.|WWW|[\w]+[' ']\d{1,5})\n(,|\D*)\s+\n(Note:)\n(.*)")

schedule = course_entry.findall(schedule_file_contents)
print(schedule)

with open(SCHEDULE_TEXT_OUTPUT_FILE, 'w', newline = '\n') as csvfile:
	schedule_writer = csv.writer(csvfile, delimiter=',')
	
    
	for course in schedule:
		schedule_writer.writerow(course)




