import sqlite3
import json
import logging
from pylocker import Locker
import uuid
import traceback

class lda(object):
    def __init__(self, dbpath):
        self.dbpath = dbpath

    def Read(self, SQL):
        lpass = str(uuid.uuid1())
        fl = Locker(self.dbpath, lockPass=lpass)
        r, dbconn, cursor = None, None, None
        try:
            acquired, code = fl.acquire_lock()
            if acquired:
                dbconn = sqlite3.connect(self.dbpath)
                dbconn.row_factory = sqlite3.Row
                cursor = dbconn.cursor()
                cursor.execute(SQL)
                r = cursor.fetchall()
            else:
                logging.error("Unable to acquire the lock. exit code %s"%code)
        except Exception as err:
            logging.error(err)
            logging.error(traceback.format_exc())
        finally:
            cursor.close()
            dbconn.close()
            fl.release_lock()

        return r

    def Update(self, SQL, args=None):
        lpass = str(uuid.uuid1())
        fl = Locker(self.dbpath, lockPass=lpass)
        r, dbconn, cursor = None, None, None
        try:
            acquired, code = fl.acquire_lock()
            if acquired:
                dbconn = sqlite3.connect(self.dbpath)
                cursor = dbconn.cursor()
                cursor.execute(SQL, args)
                r = cursor.lastrowid
                dbconn.commit()
            else:
                logging.error("Unable to acquire the lock. exit code %s"%code)
        except Exception as err:
            r = None
            dbconn.rollback()
            logging.error(err)
            logging.error(traceback.format_exc())
        finally:
            cursor.close()
            dbconn.close()
            fl.release_lock()

        return r

    def GetHistories(self):
        r = self.Read("SELECT * FROM `TagHistory` WHERE send_to = 0")

        r = json.dumps([dict(ix) for ix in r])
        r = json.loads(r)
        if len(r) > 0:
            return True, r
        else:
            return False, r

    def SwitchStatus(self, data):
        SQL = "UPDATE `TagHistory` SET send_to = ? WHERE badge = ? and user_id = ? and user_name = ? and card_id = ? and card_name = ? and com_id = ? and com_name = ? and created_on = ?"
        updated = 0
        for x in data:
            r = self.Update(SQL, (1, x['badge'], x['user_id'], x['user_name'], x['card_id'], x['card_name'], x['com_id'], x['com_name'], x['created_on']))
            if r is None:
                # Once try result fail change send status 99(Error)
                r = self.Update(SQL, (99, x['badge'], x['user_id'], x['user_name'], x['card_id'], x['card_name'], x['com_id'], x['com_name'], x['created_on']))
            else:
                updated += 1

        return updated
