import urllib2
import urllib
import cookielib
import pprint
import unicodedata
import re
from bs4 import BeautifulSoup

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

postData = urllib.urlencode({
	'timezoneOffset': '-480',
	'userid' : '1000008',
	'pwd': 'WERsdf234'
})

request = urllib2.Request(
	url = "https://myportal.sutd.edu.sg/psp/EPPRD/?cmd=login&languageCd=ENG",
	data = postData
)

# Simulate login
result = opener.open(request)

# Request my calendar
calendarUrl = "https://sams.sutd.edu.sg/psc/CSPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_LIST.GBL"
calendarData = "DERIVED_REGFRM1_SSR_SCHED_FORMAT$38$:L"
calendarResult = opener.open(calendarUrl, calendarData);
calendarHtml = calendarResult.read()
soup = BeautifulSoup(calendarHtml)

# Get the timetable and remove redundant
timeTable = soup.find_all(id="ACE_STDNT_ENRL_SSV2$0", limit=1)[0]

# print timeTable.prettify()

def extractDataFromHtmlTable(timeTable):
	coursesInfoData = {}
	# Extract information for each courses
	courseInfoTableHtml = timeTable.find_all(class_ = 'PSGROUPBOXWBO')
	for courseInfo in courseInfoTableHtml:
		courseTitle = courseInfo.find(class_ = 'PAGROUPDIVIDER').string
		# Find id which is trCLASS_MTG_VW.+
		courseScheduleTableHtml = courseInfo.find_all('tr', id=re.compile('trCLASS_MTG_VW\\$\d_row\d'))
		courseTimeSlots = []
		for row in courseScheduleTableHtml:
			timeSlot = {}
			time = row.find_all('div', id=re.compile('win0divMTG_SCHED\\$\d'))[0].get_text()
			timeSlot['time'] = time
			# win0divMTG_LOC$0
			room = row.find_all('div', id=re.compile('win0divMTG_LOC\\$\d'))[0].get_text()
			timeSlot['room'] = room
			date = row.find_all('div', id=re.compile('win0divMTG_DATES\\$\d'))[0].get_text()
			timeSlot['date'] = date
			courseTimeSlots.append(timeSlot)
		coursesInfoData[courseTitle] = courseTimeSlots
	return coursesInfoData
pprint.pprint(extractDataFromHtmlTable(timeTable))