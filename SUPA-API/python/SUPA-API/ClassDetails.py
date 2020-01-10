import requests
# currently broken on OSX, see https://github.com/lxml/lxml/pull/258
#from lxml import html

homeurl = 'https://my.supa.ac.uk/'
loginurl = 'https://my.supa.ac.uk/login/index.php'
#detailsurl = 'https://my.supa.ac.uk/user/index.php?contextid=4668&roleid=0&id=129&search&perpage=5000'
detailsurl = 'https://my.supa.ac.uk/user/index.php?contextid=4668&id=129&perpage=5000'

logindetails = {'username' : 'michaelalexander',
                'password' : raw_input('password: '),
                }

session_requests = requests.session()
loginresult = session_requests.post(loginurl,
                                    data = logindetails,
                                    headers = dict(referer=loginurl))
detailsresult = session_requests.get(detailsurl,
                                     headers = dict(referer=detailsurl))
print loginresult.content
print '******'
print detailsresult.content

def between(string, start, end) :
    istart = string.find(start) + len(start)
    beginning = string[:istart]
    string = string[istart:]
    iend = string.find(end)
    middle = string[:iend]
    finish = string[iend:]
    return beginning, middle, finish

splitdetails = detailsresult.content.split('usercheckbox')[1:]
students = {}
for details in splitdetails :
    beginning, userid, details = between(details, 'name="user', '"')
    beginning, name, details = between(details, 'course=129">', '<')
    beginning, name, details = between(details, 'course=129">', '<')
    beginning, email, details = between(details, '_c3">', '<')
    beginning, institute, details = between(details, '_c4">', '<')
    beginning, country, details = between(details, '_c5">', '<')
    
    students[int(userid)] = dict(userid = userid,
                                 name = name,
                                 email = email,
                                 institute = institute,
                                 country = country)
    
studentslist = students.values()
studentslist.sort(key = lambda student : student['name'].split()[-1])
studentslist.sort(key = lambda student : student['institute'])
for student in studentslist :
    print student['name'] + '\t' + student['email'] + '\t' + student['institute']
    
