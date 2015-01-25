import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

postData = urllib.urlencode({
	'timezoneOffset': '-480',
	'userid' : '1000227',
	'pwd': 'Summer23847601'
})

request = urllib2.Request(
	url = "https://myportal.sutd.edu.sg/psp/EPPRD/?cmd=login&languageCd=ENG",
	data = postData
)

# Simulate login
result = opener.open(request)

# # Open my timetable page
# timetableResult = opener.open('https://myportal.sutd.edu.sg/psp/EPPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W.GBL?PORTALPARAM_PTCNAV=HC_SSR_SSENRL_SCHD_W_GBL&EOPP.SCNode=EMPL&EOPP.SCPortal=EMPLOYEE&EOPP.SCName=ADMN_STUDENT_SELF_SERVICE&EOPP.SCLabel=&EOPP.SCPTcname=PT_PTPP_SCFNAV_BASEPAGE_SCR&FolderPath=PORTAL_ROOT_OBJECT.PORTAL_BASE_DATA.CO_NAVIGATION_COLLECTIONS.ADMN_STUDENT_SELF_SERVICE.ADMN_S201204261955122909329508&IsFolder=false')

# Request my calendar
calendarUrl = "https://sams.sutd.edu.sg/psc/CSPRD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W.GBL"
calendarResult = opener.open(calendarUrl)
calendarHtml = calendarResult.read()
soup = BeautifulSoup(calendarHtml)

# Get the timetable and remove redundant
timeTable = soup.find_all(id="WEEKLY_SCHED_HTMLAREA", limit=1)[0]
[duplict.extract() for duplict in timeTable.find_all(class_="SSSWEEKLYBACKGROUNDOVLP")]

print timeTable.prettify()