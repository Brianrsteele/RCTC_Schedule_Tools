import csv
import requests
import bs4
from datetime import *


class MnscuSystem:
    """A class to hold data about the MnSCU System."""

    # The base URL for MnSCU department search
    BASE_DEPT_URL = 'https://eservices.minnstate.edu/registration/search/advancedSubmit.html'

    # The base URL for the MnSCU course schedule site
    BASE_COURSE_URL = 'https://eservices.minnstate.edu/registration/search/detail.html'

    # A list of tuples with the names of MnSCU schools and their associated ID numbers
    # in the MnSCU course schedule.
    MNSCU_SCHOOLS = [('Alexandria Techncial and Community College', '0203'),
                     ('Anoka Technical College', '0202'),
                     ('Anoka-Ramsey Community College', '0152'),
                     ('Bemidji State University', '0070'),
                     ('Central Lakes College', '0301'),
                     ('Century College', '0304'),
                     ('Dakota County Technical College', '0211'),
                     ('Fond du Lac Tribal and Community College', '0163'),
                     ('Hennepin Technical College', '0204'),
                     ('Hibbing Community College', '0310'),
                     ('Inver Hills Community College', '0157'),
                     ('Itasca Community College', '0144'),
                     ('Lake Superior College', '0302'),
                     ('Mesabi Range College', '0411'),
                     ('Metropolitan State University', '0076'),
                     ('Minneapolis Community and Technical College', '0305'),
                     ('Minnesota State Community College - Southeast Technical', '0213'),
                     ('Minnesota State Community and Technical College', '0142'),
                     ('Minnesota State University Moorhead', '0072'),
                     ('Minnesota State University Mankato', '0071'),
                     ('Minnesota West Community and Technical College', '0209'),
                     ('Normandale Community College', '0156'),
                     ('North Hennepin Community College', '0153'),
                     ('Northland Community and Technical College', '0303'),
                     ('Northwest Technical College', '0263'),
                     ('Pine Technical and Community College', '0205'),
                     ('Rainy River Community College', '0155'),
                     ('Ridgewater College', '0308'),
                     ('Riverland Community College', '0307'),
                     ('Rochester Community and Technical College', '0306'),
                     ('Saint Paul College', '0206'),
                     ('South Central College', '0309'),
                     ('Southwest Minnesota State University', '0075'),
                     ('St. Cloud State University', '0073'),
                     ('St. Cloud Technical and Community College', '0208'),
                     ('Vermillion Community College', '0147'),
                     ('Winona State University', '0074')]


    # Returns the name of a school based on its MnSCU Id number
    # id is four character id number in MnSCU system, i.e. '0306' = RCTC
    def return_school_name(self, id):
        for school in self.MNSCU_SCHOOLS:
            if school[1] == id:
                return school[0]
        else:
            return "Error: No matching ID."

    def create_dept_payLoad(self, campus_id, semester_id, dept):
        """create the papameters to add to a base url to find a course at MnSCU
            currently hard coded for RCTC"""
        payload = {'campusid': campus_id, 'searchrcid': campus_id, 'searchcampusid': campus_id,
               'yrtr': semester_id, 'subject': dept, 'openValue': 'OPEN_PLUS_WAITLIST',
               'delivery': 'ALL', 'credittype': 'ALL', 'resultNumber': '250'}
        return payload

    def retrieve_department_page(self, URL, payload):
        """
        Downloads html data into r.
        """
        r = requests.get(URL, params=payload)
        r.raise_for_status()
        return r.text



class Semester:
    """A class to create semester objects accorting to the MnSCU semester format"""

    # Initialize a MnscuSystem object
    # semester should be in the MnSCU semester ID format - '20173' = Fall, 2016
    def __init__(self, semester, year):
        self.semester = semester
        self.year = year

        if self.semester == "FALL":
            self.semester_id = str(int(self.year) + 1) + '3'
        elif self.semester == "SPRING":
            self.semester_id = str(int(self.year)) + '5'
        elif self.semester == "SUMMER":
            self.semester_id = str(int(self.year) + 1) + '1'
        else:
            self.semester_id = "ERROR, incorrect semester specified"
        
        


class School:
    """A class to hold data about individual schools in the MnSCU system"""

    def __init__(self,  id, name = None, URL = None):
        self.id = id
        self.name = name
        self.URL = URL
        self.departments = []



    def __str__(self):
        return "{0}: {1}".format(self.name, self.id)


class Department:
    """A class to contain department information for a department in a MnSCU school"""
    def __init__(self, dept_name, school_id = None, school_name = None):
        self.school_name = school_name
        self.school_id = school_id
        self.dept_name = dept_name
        self.course_list = []

    def __str__(self):
        return self.dept_name

    def create_dept_payLoad(self, campus_id, semester_id, dept):
        """create the papameters to add to a base url to find a course at MnSCU
            currently hard coded for RCTC"""
        payload = {'campusid': campus_id, 'searchrcid': campus_id, 'searchcampusid': campus_id,
               'yrtr': semester_id, 'subject': dept, 'openValue': 'ALL',
               'delivery': 'ALL', 'credittype': 'ALL', 'resultNumber': '250'}
        return payload

    def retrieve_dept_page(self, URL, payload):
        """
        Downloads html data into r.
        """
        r = requests.get(URL, params=payload)
        r.raise_for_status()
        return r.text

    def retrieve_dept_data(self, dept_data):
        html_doc = dept_data
        page = bs4.BeautifulSoup(html_doc, 'html.parser')
        

        course_numbers = []

        # get course offering information from page
        table_page = page.find_all('table')
        
        course_list_table = table_page[4].find_all('td')
        
        

        for i in range(2, len(course_list_table), 14):
        	course_numbers.append(str.strip(str(course_list_table[i].get_text())))
        
        return course_numbers


class Course:
    """A class for containing course information"""

    def __init__(self, school_id, semester_id, dept_name, course_number):
        self.school_id = school_id
        self.semester_id = semester_id
        self.dept_name = dept_name
        self.course_id_number = course_number
        self.course_title = ''
        self.course_number = ''
        self.section = ''
        self.semester = ''
        self.year = ''
        self.meeting_days = ''
        self.meeting_time = ''
        self.class_size = ''
        self.enrolled = ''
        self.fill_rate = ''
        self.instructor1 = ''
        self.instructor2 = ''
        self.instructor3 = ''
        self.delivery_type = ''
        self.school_name = ''

    def createDateString(self):
        """
            return a string with today's date in yyyy-mm-dd format.
        """
        dt = datetime.now()
        dayTimeString = dt.strftime('%Y-%m-%d')
        return dayTimeString


    def create_course_pay_load(self):
        """create the papameters to add to a base url to find a course at MnSCU
                currently hard coded for RCTC
        """
        payload = {'campusid': self.school_id, 'courseid': self.course_id_number, 'yrtr': self.semester_id,
                   'rcid': self.school_id, 'localrcid': self.school_id,'partnered': 'false', 'parent': 'search'}
        return payload

    def retrieve_course_page(self, URL, payload):
        """
        Downloads html data into r.
        """
        r = requests.get(URL, params=payload)
        r.raise_for_status()
        return r.text

    def retrieve_course_data(self, course_data):
        html_doc = course_data
        page = bs4.BeautifulSoup(html_doc, 'html.parser')
        
        


        # get course offering information from page
        h1_page = page.h1.get_text()
        
        courseInfo = h1_page.split()
        
        self.course_number = str(courseInfo[1])
        self.course_title = str(' '.join(courseInfo[3:-4]))
        self.semester = str(courseInfo[-4])
        self.section = str(courseInfo[-1])
        year = str(courseInfo[-3])
        self.year = str.rstrip(year, ',')

        # get enrollment information from page
        table_page = page.find_all('table')
        scheduleData = table_page[5].find_all('td')

        # get meeting days
        days = scheduleData[1].get_text()
        days = str(days)
        days = str(days.replace('\xa0', ' '))
        days = days.strip()
        days = days.split('\n')[0:]
        days = ''.join(days)
        self.meeting_days = days

        # get schedule times
        time = scheduleData[2].get_text()
        time = str(time.replace('\xa0', ' '))
        time = time.strip()
        self.meeting_time = time

        # get enrollment data and fill rate
        enrollmentData = table_page[7].find_all('td')
        size = enrollmentData[1].get_text()
        enrolled = enrollmentData[2].get_text()
        self.class_size = str(size.split()[1])
        self.enrolled = str(enrolled.split()[1])
        self.fill_rate = str((float(enrolled.split()[1]) / float(size.split()[1])) * 100)

        # get instructor
        instructor = table_page[4].find_all('td')
        instructor = str.strip(instructor[11].get_text())
        instructor = str(instructor.replace('\xc2\xa0', ' '))
        instructor = instructor.split()

        if (len(instructor) == 6):
            self.instructor1 = instructor[0].replace(',', ', ') + instructor[1]
            self.instructor2 = instructor[2].replace(',', ', ') + instructor[3]
            self.instructor3 = instructor[4].replace(',', ', ') + instructor[5]
        elif (len(instructor) == 4):
            self.instructor1 = instructor[0].replace(',', ', ') + instructor[1]
            self.instructor2 = instructor[2].replace(',', ', ') + instructor[3]
            self.instructor3 = ' , '
        else:
            ## instructor might be listed as n/a
            if(instructor[0] == 'n/a'):
                self.instructor1 = 'n/a' + ' , ' + 'n/a'
            else:
                self.instructor1 = instructor[0].replace(',', ', ') + instructor[1]
            self.instructor2 = ' , '
            self.instructor3 = ' , '


        # get delivery type from page
        deliveryType = table_page[4].find_all('td')
        deliveryType = str.strip(deliveryType[12].get_text())
        if (deliveryType == ''):
            self.delivery_type = 'In-Person'
        else:
            self.delivery_type = str(deliveryType)

        # get school
        school = table_page[6].find_all('td')
        school = str.strip(school[-2].get_text().split(':')[1])
        self.school_name = str(school)

        # calculate fill rate
        self.fill_rate = '{:0.2f}'.format((int(self.enrolled)/int(self.class_size)) *  100)

        course_array = {'date': self.createDateString(), 'academicYear': self.year, 'semester': self.semester,
                        'school': self.school_name, 'dept': self.dept_name, 'course number': self.course_number,
                        'title': self.course_title, 'section': self.section, 'days': self.meeting_days,
                        'time': self.meeting_time, 'size': self.class_size, 'enrolled': self.enrolled,
                        'delivery': self.delivery_type, 'lastName1': self.instructor1.split(',')[0],
                        'firstName1': self.instructor1.split(',')[1], 'lastName2': self.instructor2.split(',')[0],
                        'firstName2': self.instructor2.split(',')[1], 'lastName3': self.instructor3.split(',')[0],
                        'firstName3': self.instructor3.split(',')[1], 'fillRate': self.fill_rate}

        return course_array



class FacultyMember:
    """A base class for defining faculty"""

    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def __str__(self):
        return self.last_name + ', ' + self.first_name


class DailyReportCreator:
    """A class that generates a dashboard from the daily data"""

    def __init__(self, data_array):
        self.data_array = data_array

    def create_report(self):

        # Create filled-seats pie chart
        values = [0,0]
        labels = ['Available Seats', 'Enrolled Seats']
        colors = ['gold', 'blue']
        for section in self.data_array:
            empty_seats = int(section['size']) - int(section['enrolled'])
            values[0] = values[0] + empty_seats
            values[1] = values[1] + int(section['enrolled'])
        plt.figure(1)
        plt.subplot(111)
        plt.pie(values, labels = labels, colors = colors, autopct = '%1.1f%%',
                shadow='true', textprops= {'color': 'white','fontsize': 'x-large'})
        plt.axis('equal')

        #create a list of courses
        list_of_courses = []
        course_enrollment = [0]
        for section in self.data_array:
            course_name = section['dept'] + ' ' + section['course number'] + ', ' + section['title']
            if course_name in list_of_courses:
                break
            else: list_of_courses.append(course_name)


        plt.show()




def main():

    mnscu = MnscuSystem()
    semester = Semester('SPRING', '2020')
    input_file = '/Users/yv3584fj/OneDrive - MNSCU/Enrollment Data/Scripts/RCTC_ART_search.csv'
    output_file = '/Users/yv3584fj/OneDrive - MNSCU/Enrollment Data/Scripts/SPRING_2020_RCTC_ART_data.csv'
    daily_data_array = []



    with open(input_file, newline = '') as csv_file:
        name_reader = csv.reader(csv_file, delimiter = ',', quotechar = '|')
        for row in name_reader:
            school = School(row[0], mnscu.return_school_name(row[0]))
            department = Department(row[1], school.id, school.name)

            pay_load = department.create_dept_payLoad(school.id, semester.semester_id, department.dept_name)
            
            
        
            dept_data = department.retrieve_dept_page(mnscu.BASE_COURSE_URL, pay_load)
            
            
            sorted_dept_data = department.retrieve_dept_data(dept_data)
           
            for i in sorted_dept_data:
                course_id_number = i
                course = Course(school.id, semester.semester_id, department.dept_name, course_id_number)
                course_pay_load = course.create_course_pay_load()
                course_data = course.retrieve_course_page(mnscu.BASE_COURSE_URL, course_pay_load)
                sorted_course_data = course.retrieve_course_data(course_data)

                with open(output_file, 'a') as csv_file:
                    fieldnames = ['date', 'academicYear', 'semester', 'school', 'dept', 'course number',
                                  'title', 'section', 'days', 'time', 'size', 'enrolled', 'delivery',
                                  'lastName1', 'firstName1', 'lastName2', 'firstName2', 'lastName3',
                                  'firstName3', 'fillRate']
                    writer = csv.DictWriter(csv_file, fieldnames = fieldnames, dialect = 'excel')
                    writer.writerow(sorted_course_data)
                csv_file.close()
                daily_data_array.append(sorted_course_data)

	





main()
