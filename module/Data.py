import sqlite3
import threading
import os.path
import datetime
import json
import traceback

def Verify(Log4s, lock, card):
	try:
		lock.acquire()
		# database connection create and query
		with open('data/account.json', 'r') as fs:
			json_data = json.load(fs)

		result = None

		for x in json_data:
			if x['card_name'] == card:
				result = x

		if(result == None):
			return (False, None)
		else:
			return (True, result)
	except Exception as err:
		Log4s.err('DataVerify', str(type(err)) + "\r\n" + traceback.format_exc())
	finally:
		lock.release()

def CheckTime(Log4s, dbpath, lock, data):
	try:
		lock.acquire()
		# Create issue time
		TickTime = datetime.datetime.now().isoformat()

		# database connection create and query
		dbconn = sqlite3.connect(dbpath)
		dbconn.row_factory = sqlite3.Row

		cursor = dbconn.cursor()
		cursor.execute("INSERT INTO `TagHistory` VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(data['user_id'], data['user_name'], data['card_id'], data['card_name'], data['com_id'], data['com_name'], TickTime, 0))
			
		result = cursor.lastrowid

		dbconn.commit()
		dbconn.close()

		if(result == None):
			return (False, None)
		else:
			return (True, result)
	except Exception as err:
		Log4s.err('HistoryInput', str(type(err)) + "\r\n" + traceback.format_exc())
	finally:
		lock.release()
		return (False, None)

def SelectHistory(Log4s, dbpath, lock):
	result = None
	rbool = False
	try:
		lock.acquire()
		dbconn = sqlite3.connect(dbpath)
		dbconn.row_factory = sqlite3.Row

		cursor = dbconn.cursor()
		cursor.execute("SELECT * FROM `TagHistory` WHERE send_to = 0")

		result = cursor.fetchall()
		dbconn.commit()
		dbconn.close()

		if(len(result) == 0):
			rbool = False
		else:
			rbool = True

	except Exception as err:
		Log4s.err('HistoryOutput', str(type(err)) + "\r\n" + traceback.format_exc())

	finally:
		lock.release()
		return (rbool, json.dumps([dict(ix) for ix in result]))

def ChangeStatus(Log4s, dbpath, lock, data):
	try:
		lock.acquire()
		# Create issue time
		TickTime = datetime.datetime.now().isoformat()

		# database connection create and query
		dbconn = sqlite3.connect(dbpath)
		dbconn.row_factory = sqlite3.Row

		cursor = dbconn.cursor()
		cursor.execute("UPDATE `TagHistory` SET send_to = 1 WHERE user_id = ? and user_name = ? and card_id = ? and card_name = ? and com_id = ? and com_name = ? and created_on = ?",(data['user_id'], data['user_name'], data['card_id'], data['card_name'], data['com_id'], data['com_name'], data['created_on']))
			
		result = cursor.lastrowid

		dbconn.commit()
		dbconn.close()

		if(result == None):
			return (False, None)
		else:
			return (True, result)
	except Exception as err:
		Log4s.err('HistoryInput', str(type(err)) + "\r\n" + traceback.format_exc())
	finally:
		lock.release()
		return (False, None)