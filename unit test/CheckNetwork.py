import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://wqq.innovatorschool.com/testrfid.aspx',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False


if internet_on() == True :
    print "Connected"
else:
    print "Not Connected"

