import xml.etree.ElementTree as ET
from xml.dom import minidom
from copy import deepcopy
import csv
import sys
import time



overlap_dict = {"0": [], "1": [], "2": [], "3": [], "4": [], "5": [], "6": []}

color_list = ["#444", "#888", "#AAA", "#CCC", "#DDD" ]

DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri"]
TABLE_WIDTH = 11 * 300
TABLE_HEIGHT = 8.5 * 300
NUM_COLUMNS = len(DAYS_OF_WEEK)
BORDER = 100
COLUMN_WIDTH = round(((TABLE_WIDTH - TABLE_WIDTH // 7) - (BORDER * 2)) // NUM_COLUMNS)
HEADER_HEIGHT = round(TABLE_HEIGHT // 20)
BASE_STROKE = round(TABLE_WIDTH * 0.002)
FONT_SIZE = '30'

#start time must be in 24 hr format - i.e. 2100
START_TIME = 700
#end time must be in 24 hr format - i.e. 2100
END_TIME = 2200
NUM_ROWS = round((END_TIME - START_TIME) // 100)
ROW_HEIGHT = round(((TABLE_HEIGHT - (BORDER * 2)) - HEADER_HEIGHT) // NUM_ROWS)
PIXELS_PER_MINUTE = ROW_HEIGHT / 60


def create_online_list(svg, table_width, border, header_height, row_height, c_width, online_list):

	online_group = ET.SubElement(
		svg,
		'g',
		attrib={
			"id": "online"
		})

	online = ET.SubElement(
				online_group,
				'text',
				attrib={
					"x": str(round((table_width - table_width // 7) - border // 2)),
					"y": str(round(border + (header_height * 0.7))),
					"font-size": str(round(header_height * 0.5)),
					"font-family": "Helvetica, sans-serif",
					"fill": "black",
					"class": "header"
				})
	online.text = "Online"
	
	count = 0
	for session in online_list:
		x_pos = str(round((table_width - table_width // 7) - border))
		y_pos = str((border + header_height + (row_height * count)))
		
		online_course_group = ET.SubElement(
		online_group,
		'g',
		attrib={
			"class": session[1].split("-")[0] + " " + session[1] + " " + session[2] + " " + session[3] + " " + session[4] + " " + session[9]
		})
		
		class_session = ET.SubElement(
			online_course_group,
			"rect",
			attrib={
				"x": x_pos,
				"y": y_pos,
				"width": str(c_width - border // 2),
				"height": str(row_height),
				"fill": session[8][0],
			})
		
		
		class_info = ET.SubElement(
			online_course_group,
			'text',
			attrib={
				"x": str(int(x_pos) + 10),
				"y": str(int(y_pos) + 40),
				"font-size": FONT_SIZE,
				"font-family": "Helvetica, sans-serif",
				"fill": "white",
				
			})
			
		class_info.text = session[1] + "-" + session[2]
	
		course_name = ET.SubElement(
			online_course_group,
			'text',
			attrib={
				"x": str(int(x_pos) + 10),
				"y": str(int(y_pos) + 70),
				"font-size": FONT_SIZE,
				"font-family": "Helvetica, sans-serif",
				"fill": "white",
				
			})
			
		course_name.text = session[10]
		
		instructor_info = ET.SubElement(
			online_course_group,
			'text',
			attrib={
				"x": str(int(x_pos) + 10),
				"y": str(int(y_pos) + 100),
				"font-size": FONT_SIZE,
				"font-family": "Helvetica, sans-serif",
				"fill": "white",
				
			})
			
		
		if session[9] == "P":
			status_text = "P"
		else:
			status_text = ""
		instructor_info.text = session[3] + " " + session[4] + " " + status_text
			
		#class_info = ET.SubElement(
		#	session_label,
		#	'tspan',
		#	attrib={
		#		'dx': '17',
		#		'dy': '40'
		#	})
			
		#course_name_info = ET.SubElement(
		#		session_label,
		#		'tspan',
		#		attrib={
		#			'dx': '-140',
		#			'dy': '25'
		#		})	
			
		#instructor_info = ET.SubElement(
		#	session_label,
		#	'tspan',
		#	attrib={
		#		'dx': '-145',
		#		'dy': '35'
		#	})
			
		
			
		
		#course_name_info.text = session[10]
		#class_info.text = session[1] + "-" + session[2]
		#if session[9] == "P":
		#	status_text = "P"
		#else:
		#	status_text = ""
		#instructor_info.text = session[3] + " " + session[4] + " " + status_text
		
		count += 1
		

def apply_fill_color(schedule_list, online_list, color_list):
	"""
		applies a color from the color list to each section on the schedule list
		:param schedule_list, a list of sections in tuple form.
		:param color_list, a list of strings holding HTML colors in hex
		:return none
	"""
	count = 0
	for i in schedule_list:
		if count >= len(color_list):
			count = 0
		i[8][0] = color_list[count]
		count += 1
		
	count = 0
	for i in online_list:
		if count >= len(color_list):
			count = 0
		i[8][0] = color_list[count]
		count += 1

def draw_row_labels(element, border, h_height, c_width, start_time, end_time,
																				num_rows, row_height):
	"""
		Draws the time at the end of each row, i.e. "0700, 0800, etc"
		:param element, the eTree XML object that will contain the row labels. In this
										case, should be the top level svg object.
		:param border, int, the width of the border around the table.
		:param h_height, int, the height of the header row for the table
		:param c_width, int, the width of the columns in the table
		:param start_time, int, the starting time for each day in the table, i.e. 700
		:param end_time, int the ending time for each day in the table, i.e. 2200
		:param num-rows, int the number of rows in each day - should be (end_time - start_time)//100
		:param row_height, int the height of each row in pixels
		:return none
	"""
	
	# Create group for row labels
	row_labels_group = ET.SubElement(
		svg,
		'g',
		attrib={
			"id": "row_labels"
		})
	for row in range(num_rows):
		day = ET.SubElement(
			row_labels_group,
			'text',
			attrib={
				"x": str(round(border + 10)),
				"y": str(round(border + h_height + (row * row_height) + 35)),
				"font-size": "30px",
				"font-family": "Helvetica, sans-serif",
				"fill": "black",
				"class": "time"
			})
		day.text = str(start_time + (100 * row))

def determine_overlap(start_time_a, end_time_a, start_time_b, end_time_b):
	"""
		Given two sections from the schedule list, determions if the sections overlap in time.
		:param start_time_a, string the start time of the first section i.e. "1000"
		:param end_time_a, string the end time of the first section i.e. "1150"
		:param start_time_b, string the start time of the second section i.e. "0900"
		:param end_time_b, string the end time of the second section i.e. "1050"
		:return, true if
							the sections start at the same time
							the first section starts after the second section starts and the second section ends after the first section ends
							the first section starts before the second section starts and the first section ends after the second section ends
							the first section starts aftger the second section starts and the first section ends after the second section ends
							the sections end at the same time
						otherwise false
	"""
	if int(start_time_a) == int(start_time_b):
		return True
	elif int(start_time_a) > int(start_time_b) and int(end_time_b) > int(
			start_time_a):
		return True
	elif int(start_time_a) < int(start_time_b) and int(end_time_a) > int(
			start_time_b):
		return True
	elif int(start_time_a) < int(start_time_b) and int(end_time_a) > int(
			end_time_b):
		return True
	elif int(start_time_a) > int(start_time_b) and int(end_time_a) < int(
			end_time_b):
		return True
	elif int(end_time_a) == int(end_time_b):
		return True
	else:
		return False

def offset_days(schedule_list, days_of_week):
	"""
		Sections in the section list store days of the week as integers with 0 == monday.
		To match up the class meeting dates with the days of the week listed for the time table,
		the integer values of the section meeting days need to be offset to match the order of the
		time table.
		:param schedule_list, list of sections in tuple form
		:param days_of_week, list of strings holding the three letter abbreviations for the days of the week.
						will be used to create the columns in the time table.
		:return none
	"""
	for section in schedule_list:
		for meeting_day in range(len(section[0])):
			if days_of_week[0] == "Sun":
				day_translation = [6, 0, 1, 2, 3, 4, 5]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])
			elif days_of_week[0] == "Mon":
				day_translation = [0, 1, 2, 3, 4, 5, 6]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])
			elif days_of_week[0] == "Tue":
				day_translation = [1, 2, 3, 4, 5, 6, 0]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])
			elif days_of_week[0] == "Wed":
				day_translation = [2, 3, 4, 5, 6, 0, 1]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])
			elif days_of_week[0] == "Thu":
				day_translation = [3, 4, 5, 6, 0, 1, 2]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])
			elif days_of_week[0] == "Fri":
				day_translation = [4, 5, 6, 0, 1, 2, 3]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])
			elif days_of_week[0] == "Sat":
				day_translation = [5, 6, 0, 1, 2, 3, 4]
				section[0][meeting_day] = day_translation.index(section[0][meeting_day])

def startSort(tuple):
	"""
		indicates what part of the section tuple to use as a key to sort the overlap dictionary
		:param tuple, tuple containting information about a section
		:return string the 5th element of the section tuple, which holds the start time for the section
	"""
	return tuple[5]

def sort_schedule_list(overlap_dict, schedule_list, days_of_week):
	"""
		Sorts the section meeting times into a dictionary that models days of the week using keys 0 - 6. In each day
		of the week the section meeting times are organized by start time, and then any overlapping sections are
		stored in the 7th element of the section tuple.
		:param overlap_dict, dictionary with keys 0 - 7 modeling the days of a week
		:param schedule_list, list with tuples holding information about the sections offered
		:param days_of_week, list of strings holding the days of the week displayed on the calendar
		:return none
	"""

	# First, align the sections meeting days (ints in the 0th element of the tuple, where 0 == monday), with the
	# days of the week listed in time table
	offset_days(schedule_list, days_of_week)

	# Sorts all of the sections into a dictionary called overlap_dict, which has keys representing the days of the week
	# where 0 == monday	(will make a copy of the section for each day that it meets, which is stored in the 0th element of the section tuple).
	for i in range(len(overlap_dict)):
		for j in range(len(schedule_list)):
			if i in schedule_list[j][0]:
				overlap_dict[str(i)].append(deepcopy(schedule_list[j]))

	# Then sorts all of the sections by start time in each of the day keys (0 - 7).
	for key in overlap_dict:
		overlap_dict[key].sort(key=startSort)

	# for each section listed in each key of the dictionary, determines if any sections overlap.
	# if they do, they are listed in the 7th element of the section tuple as department, course, and section,
	# i.e "Art 1184-01"
	for key in overlap_dict:
		for i in overlap_dict[key]:
			for j in overlap_dict[key]:
				if determine_overlap(i[5], i[6], j[5], j[6]):
					i[7].append(j[1] + "-" + j[2])

def compute_meeting_length_in_minutes(meeting_start_time, meeting_end_time):
	"""
		Given two meeting start times in 24 hour format, compute the total number of minutes a section meets
		:param meeting_start_time, string holding the start time of a section in 24 hour format ("1150")
		:param meeting_end_time, string holding the end time of a section in 24 hour format ("0900")
		:return int the time in minutes that the session meets
		:raise exception if the meeting ends before the start
	"""
	
	print(meeting_start_time, meeting_end_time, "----------------------")
	if int(meeting_end_time) > int(meeting_start_time):
		minutes = int(meeting_end_time[-2:]) - int(meeting_start_time[-2:])
		hours = int(meeting_end_time[0:2]) - int(meeting_start_time[0:2])
		minutes = abs(minutes) + (hours * 60)
		
		return minutes
	else:
		raise Exception("The meeting end time must be after the meeting start time")

def draw_columns(element, num_columns, t_height, c_width, border, stroke):
	"""
		Draw columns for the days in the time table.
		:param element, eTree element object that will be the parent of the columns
		:param num_columns, int the number of column (or days) in the time table
		:param t_height, int the height of the table in pixels
		:param c_width, int the width of each column in pixels
		:param border, int the width of the borders around the table in pixels
		:param stroke: int the width of the stroke in pixels
		:return none
	"""
	
	# create a group for the column lines
	column_group = ET.SubElement(
		svg,
		'g',
		attrib={
			"id": "columns"
		})
	
	for i in range(0, num_columns + 1):
		line = ET.SubElement(
			column_group,
			'line',
			attrib={
				"x1": str(round(border + (i * c_width))),
				"y1": str(border),
				"x2": str(round(border + (i * c_width))),
				"y2": str(round(t_height - border)),
				"stroke": "black",
				"stroke-width": str(stroke),
				"class": "table_column_line"
			})

def draw_headers(element, border, num_columns, header_height, column_width,
																	table_height, days_of_week, stroke):
	"""
		Draw text labels for the timetable days, including boxes around headers and a line at the bottom of the table
		:param element, eTree element object that will be the parent of the columns
		:param num_columns, int the number of column (or days) in the time table
		:param header_height, int the height of the table header in pixels
		:param column_width, int the width of each column in pixels
		:param table_height, int the height of the table in pixels
		:param days_of_week, list holding strings with the names of each day in the week
		:param stroke: int the width of the stroke in pixels
		:return none
	"""
	
	# Group the header elements in a g tag
	header_group = ET.SubElement(
		svg,
		'g',
		attrib={
			"id": "table_header"
		})

	# Draw the top line of the header
	header_top = ET.SubElement(
		header_group,
		'line',
		attrib={
			"x1": str(border),
			"y1": str(border),
			"x2": str(border + (num_columns * column_width)),
			"y2": str(border),
			"stroke": "black",
			"stroke-width": str(stroke),
			"class": "header_top"
		})

	# Draw the bottom line of the header
	header_bottom = ET.SubElement(
		header_group,
		'line',
		attrib={
			"x1": str(border),
			"y1": str(border + header_height),
			"x2": str(border + (num_columns * column_width)),
			"y2": str(border + header_height),
			"stroke": "black",
			"stroke-width": str(stroke),
			"class": "header_bottom"
		})

	# Draw the bottom line of the table
	table_bottom = ET.SubElement(
		header_group,
		'line',
		attrib={
			"x1": str(border),
			"y1": str(table_height - border),
			"x2": str(border + (num_columns * column_width)),
			"y2": str(table_height - border),
			"stroke": "black",
			"stroke-width": str(stroke),
			"class": "table_bottom"

		})

	# Draw lines to indicate columns for each day of the week
	for i in range(0, len(days_of_week)):
		day = ET.SubElement(
			header_group,
			'text',
			attrib={
				"x": str(round(border + (column_width * i) + (column_width * 0.10))),
				"y": str(round(border + (header_height * 0.7))),
				"font-size": str(round(header_height * 0.5)),
				"font-family": "Helvetica, sans-serif",
				"fill": "black",
				"class": "header"
			})
		day.text = days_of_week[i]

def draw_rows(num_rows, border, r_height, h_height, t_width, base_stroke):
	"""
		Draw lines for horizontal rows
		:param num_rows, int the number of rows representing hours in the day
		:param border, int the number of pixels between the edge of the image and the outside lines of the time table.
		:param r_height, int height of each row in pixels
		:param h_height, int the height of the table header in pixels
		:param t_widht, int the width of the table in pixels
		:param base_stroke, int the size in pixels of the base_stroke. Some of the other strokes will be sized in relation to the
									base_stroke
		:return none
	"""
	
	row_group = ET.SubElement(
		svg,
		'g',
		attrib={
			"id": "rows"
		})
	
	for i in range(0, num_rows):
		line = ET.SubElement(
			row_group,
			'line',
			attrib={
				"x1": str(border),
				"y1": str((r_height * i) + border + h_height),
				"x2": str(t_width - border),
				"y2": str((r_height * i) + border + h_height),
				"stroke": "black",
				"stroke-width": str(base_stroke // 4),
				"class": "table_row_line"

			})

def draw_meeting_times(overlap_dict, c_width, border, h_height, s_time,
														r_height, pixels_per_minute):
	"""
		Draw rectangles for each of the meeting times for each of the sections
		:param overlap_dict, dict with keys 0-7 representing the meeting days of the week, with each key holding
					a list of sections organized by start time.
		:param c_width, int holding the width in pixels of each column in the time table
		:param border, int holding the space in pixels between the edge of the image and the outside edges of the time table
		:param h_height, int holding the height in pixels of the table header
		:param s_time, int holding the starting time of the days in the time table in 24 hour format, i.e. 700
		:param r_height, int holding the height of each row in pixels
		:param pixels_per_minute, int holding the number of pixels that each minute of the time table needs to accurately
						represent the length of the class
	"""
	
	
	
	for key in overlap_dict:
		for session in overlap_dict[key]:
			x_pos = str(((c_width * int(key)) + border) + (session[7].index(session[1] + "-" + session[2]) * c_width // len(session[7])))
			y_pos = str(border + h_height + (((int(session[5]) - s_time) // 100) * r_height))
			
			session_group = ET.SubElement(
				svg,
				'g',
				attrib={
					"class": session[1].split("-")[0] + " " + session[1] + " " + session[2] + " " + session[3] + " " + session[4] + " " + session[9]
				})
			
			class_session = ET.SubElement(
				session_group,
				"rect",
				attrib={
					"x": x_pos,
					"y": y_pos,
					"width":
					str(c_width // len(session[7])),
					"height":
					str(
						compute_meeting_length_in_minutes(session[5], session[6]) *
						pixels_per_minute),
					"fill": session[8][0],
				})
			
			session_label = ET.SubElement(
				session_group,
				'g',
				attrib={
					"x": x_pos,
					"y": y_pos,
					"font-size": FONT_SIZE,
					"font-family": "Helvetica, sans-serif",
					"fill": "white",
					"class": session[1].split("-")[0] + " " + session[1] + " " + session[2] + " " + session[3] + " " 
							+ session[4] + " " + session[9],
					"transform": "rotate(90 " + x_pos + " " + y_pos + ") translate(20 -80)"
				})
			
			
			class_info = ET.SubElement(
				session_label,
				'text',
				attrib={
					"x": x_pos,
					"y": y_pos,
					"font-size": FONT_SIZE,
					"font-family": "Helvetica, sans-serif",
					"fill": "white",
					#"transform": "rotate(90 " + x_pos + " " + y_pos + ") translate(20 -60)"
				})
			
			class_info.text = session[1] + "-" + session[2]
			
			course_name = ET.SubElement(
			session_label,
			'text',
			attrib={
				"x": x_pos,
					"y": y_pos,
					"font-size": FONT_SIZE,
					"font-family": "Helvetica, sans-serif",
					"fill": "white",
					"dy" : '30',
				
			})
			
			course_name.text = session[10]
			
			instructor_info = ET.SubElement(
				session_label,
					'text',
					attrib={
					"x": x_pos,
					"y": y_pos,
					"font-size": FONT_SIZE,
					"font-family": "Helvetica, sans-serif",
					"fill": "white",
					"dy" : '60'
				})

			
			if session[9] == "P":
				status_text = "P"
			else:
				status_text = ""
			instructor_info.text = session[3] + " " + session[4] + " " + status_text

# --------------------------------------------------------------------!
# this bit for importing from a csv file
# --------------------------------------------------------------------!

# import CSV file

schedule_list = []

online_list = []

with open(sys.argv[1], newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar="|")
	for row in reader:
		status = row[6]
		title = row[4]
		days = row[7].split()
		days_converted = []
		for day in days:
			if "M" in day:
				days_converted.append(0)
			if "T" in day:
				days_converted.append(1)
			if "W" in day:
				days_converted.append(2)
			if "H" in day:
				days_converted.append(3)
			if "F" in day:
				days_converted.append(4)
			if "S" in day:
				days_converted.append(5)
		course_label = row[1] + "-" + row[2]
		course_section = row[3]
		instructor_name = row[11][1:]
		room = row[10]
		
		# convert start time to 24 hour time
		
		if row[8] != 'ARR':
			# create a time object from a string in format '8:54 PM'
			temp_time = time.strptime(row[8], '%I:%M %p')
			# export a string from a time object in the format '2054'
			start_time = time.strftime('%H%M', temp_time )			
		else:
			start_time = 'ARR'	
			
		if row[9] != 'ARR':
			# create a time object from a string in format '8:54 PM'
			temp_time = time.strptime(row[9], '%I:%M %p')
			# export a string from a time object in the format '2054'
			end_time = time.strftime('%H%M', temp_time )	
		else:
			end_time = 'ARR'
		
		# convert end time to 24 hour time
		
		print(start_time, end_time, course_label)	
		
		if row[9] == "ARR":
			online_list.append((days_converted,
							course_label,
							course_section,
							instructor_name, 
							room, 
							start_time, 
							str(end_time),
							[], 
							[""],
							status,
							title))
		
		else:
			schedule_list.append((days_converted,
								course_label,
								course_section,
								instructor_name, 
								room, 
								start_time, 
								str(end_time),
								[], 
								[""],
								status,
								title))




print("online list -----------------------")
for section in online_list:
	print(section)
	
print("schedule list -----------------------")
for section in schedule_list:
	print(section)


# --------------------------------------------------------------------!

# Start the svg document
svg = ET.Element(
	'svg',
	attrib={
		"version": "1.1",
		"baseProfile": "full",
		"width": str(TABLE_WIDTH),
		"height": str(TABLE_HEIGHT),
		"xmlns": "http://www.w3.org/2000/svg"
	})
	


		


# Give each section a color
apply_fill_color(schedule_list, online_list, color_list)

# Sort the schedule list to create the overlap_dict
sort_schedule_list(overlap_dict, schedule_list, DAYS_OF_WEEK)

# Draw the table rows
draw_rows(NUM_ROWS, BORDER, ROW_HEIGHT, HEADER_HEIGHT, (TABLE_WIDTH - TABLE_WIDTH // 7),
										BASE_STROKE)

# Draw the label rows
draw_row_labels(svg, BORDER, HEADER_HEIGHT, COLUMN_WIDTH, START_TIME, END_TIME,
																NUM_ROWS, ROW_HEIGHT)

# Draw the meeting times as rectangles
draw_meeting_times(overlap_dict, COLUMN_WIDTH, BORDER, HEADER_HEIGHT,
													START_TIME, ROW_HEIGHT, PIXELS_PER_MINUTE)


# Create the online classes section

create_online_list(svg, TABLE_WIDTH, BORDER, HEADER_HEIGHT, ROW_HEIGHT, COLUMN_WIDTH, online_list)


# Draw the column lines
draw_columns(svg, NUM_COLUMNS, TABLE_HEIGHT, COLUMN_WIDTH, BORDER, BASE_STROKE)




# Draw the table header
draw_headers(svg, BORDER, NUM_COLUMNS, HEADER_HEIGHT, COLUMN_WIDTH,
													TABLE_HEIGHT, DAYS_OF_WEEK, BASE_STROKE)
													

# Convert the eTree information for the svg file to a string for writing to a file
svg_data = ET.tostring(svg, encoding="unicode")

# parses the data of the element tree to make it easier to pretty print with tabs and
# newlines
reparsed_svg_data = minidom.parseString(svg_data)

# Open the file for writing the svg data. At some point this should use the department as the name of the file.
svg_file = open(sys.argv[1][:-4] + '.svg', "w")

# Write the svg data to the file, pretty printed with indents and newlines
svg_file.write(reparsed_svg_data.toprettyxml(indent="    "))

# Close the file
svg_file.close()

# Add link to external stylesheet

svg_file = open(sys.argv[1][:-4] + '.svg', "r+")
old = svg_file.read()
svg_file.seek(22, 0)
svg_file.write('\n<?xml-stylesheet type="text/css" href="styles.css" ?>'+ old[22:])
svg_file.close()

