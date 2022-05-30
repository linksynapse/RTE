import argparse
import logging
from logging import handlers
import json
import lda, c7941w, acs
import uuid
from pylocker import Locker
import os, time
import traceback

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create new database tool')
    parser.add_argument('-c','--component', type=str ,help='component for rs232', required=True)
    parser.add_argument('-b','--baudrate', type=int ,help='baudrate for rs232', required=True)
    parser.add_argument('-l','--log', type=str ,help='logging output file path', default=os.environ.get('LOG_PATH', '/var/log/hsyc.d.log'))
    parser.add_argument('-d','--db', type=str ,help='history db file path', default=os.environ.get('HISTORY_PATH', '/opt/data/history.dat'))
    parser.add_argument('-u','--user', type=str ,help='user data output file path', default=os.environ.get('DATA_PATH', '/opt/data/account.json'))
    args = parser.parse_args()

    rfh = logging.handlers.RotatingFileHandler(
        filename=args.log,
        mode='a',
        maxBytes=1024*1024*20,
        backupCount=2,
        encoding='utf-8',
        delay=0
    )
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        datefmt='%m%d/%Y %I:%M:%S %p',
        handlers=[
            rfh
        ]
    )

    try:
        ilda = lda.lda(args.db)
        ic7941 = c7941w.c7941w(args.component, args.baudrate)
        iacs = acs.acs()

        iacs.PlayLoadComplate()
        while True:
            ldata = ic7941.GetEM()
            if ldata != 0:
                lpass = str(uuid.uuid1())
                fl = Locker(args.user, lockPass=lpass)
                json_data, result = None, None
                try:
                    acquired, code = fl.acquire_lock()
                    if acquired:
                        with open(args.user,'r',encoding='utf-8') as fs:
                            json_data = json.load(fs)

                        for x in json_data:
                            if x['card_name'] == ldata:
                                result = x
                    else:
                        logging.error("Unable to acquire the lock. exit code %s"%code)
                except Exception as err:
                    logging.error(err)
                finally:
                    fl.release_lock()
                    

                    if result is not None:
                        result, ldata = ilda.CheckInUser(result)
                        if result:
                            logging.info('CheckIn data store successful rowid -> %d', ldata)
                            iacs.OnBlue()
                            iacs.FulldownExt1()
                            iacs.PlaySuccess()
                        else:
                            logging.error('CheckIn data store fail')
                    else:
                        iacs.OnRed()
                        iacs.FulldownExt2()
                        iacs.PlayFail()
            else:
                pass

            iacs.ClearLed()
            iacs.RaisingAll()
    except KeyboardInterrupt as ki:
        logging.info('Interrupt from user')
    except Exception as err:
        logging.error(err)
        logging.error(traceback.format_exc())
    finally:
        logging.info('exit program.')