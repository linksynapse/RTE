import sqlite3
import os.path
import datetime
import json

class Manager:
	def __init__(self, config):
		self.path = config.Database()
		self.db = sqlite3.connect(self.path)

	def __del__(self):
		self.db.close()


	def Verify(self, Card):
		# database connection create and query
		with open('data/account.json', 'r') as fs:
			json_data = json.load(fs)

		result = None

		for x in json_data:
			if x['CardNumber'] == Card:
				result = (x['Badge'],x['Name'],x['CardNumber'])

		if(result == None):
			return (False, None)
		else:
			return (True, result)

	def CheckTime(self, data):
		# Create issue time
		TickTime = datetime.datetime.now().timestamp()

		# database connection create and query
		db = sqlite3.connect(self.path)
		cursor = db.cursor()
		cursor.execute("INSERT INTO `User.History` (Badge, Card, Time) VALUES (?, ?, ?)",(data[0], data[2], TickTime,))
		db.commit()

		result = cursor.lastrowid
		cursor.close()

		if(result == None):
			return (False, None)
		else:
			return (True, result)

	def DoneSendHistory(self, data):
		db = sqlite3.connect(self.path)
		cursor = db.cursor()
		cursor.execute("UPDATE `User.History` SET Sended = 1 WHERE Badge = ? AND Card = ? AND Time = ?",(data[0],data[1],data[2],))
		db.commit()

		result = cursor.lastrowid
		cursor.close()

		if(result == None):
			return (False, None)
		else:
			return (True, result)

	def SelectHistory(self):
		cursor = self.db.cursor()
		cursor.execute("SELECT * FROM `User.History` WHERE Sended = 0 LIMIT 1")
		result = cursor.fetchone()
		cursor.close()

		if(result == None):
			return (False, None)
		else:
			return (True, result)
		