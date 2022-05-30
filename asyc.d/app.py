import argparse
import logging
from logging import handlers
import json
import rda
import uuid
import os, time
from pylocker import Locker
import tools
import traceback

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create new database tool')
    parser.add_argument('-r','--remote', type=str ,help='api server host', required=True)
    parser.add_argument('-p','--port', type=int ,help='api server port', required=True)
    parser.add_argument('-l','--log', type=str ,help='logging output file path', default=os.environ.get('LOG_PATH', '/var/log/asyc.d.log'))
    parser.add_argument('-o','--out', type=str ,help='user data output file path', default=os.environ.get('DATA_PATH', '/opt/data/account.json'))
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
        irda = rda.rda(args.remote + ':' + str(args.port))

        while True:
            start = time.time()
            cpu_id = tools.GetCPUID()
            nataddr = tools.GetNATIPaddress()
            macaddr = tools.GetMacAddress()
            cpu_usage = tools.GetCPUUsage()
            disk_usage = tools.GetDiskUsage()
            ram_usage = tools.GetRamUsage()
            wifi_ssid = tools.GetWIFISSID()
            wifi_quality = tools.GetWIFIQuality()
            temp = tools.GetTemp()

            result, rdata = irda.DownloadDeviceInform(
                cpu_id=cpu_id, 
                nataddr=nataddr, 
                macaddress=macaddr, 
                cpu_usage=cpu_usage, 
                disk_usage=disk_usage, 
                ram_usage=ram_usage, 
                temp=temp, 
                wifi_quality=wifi_quality,
                wifi_ssid=wifi_ssid
            )
            if result:
                result, rdata = irda.DownloadUser(rdata[0]['proj_id'])
                if result:
                    lpass = str(uuid.uuid1())
                    fl = Locker(args.out, lockPass=lpass)
                    try:
                        acquired, code = fl.acquire_lock()
                        if acquired:
                            with open(args.out,'w',encoding='utf-8') as fs:
                                json.dump(rdata, fs, indent="\t")
                        else:
                            logging.error("Unable to acquire the lock. exit code %s"%code)
                    except Exception as err:
                        logging.error(err)
                    finally:
                        fl.release_lock()
            logging.info('finish job. %s sec', time.time() - start)
            time.sleep(60)
    except Exception as err:
        logging.error(err)
        logging.error(traceback.format_exc())
    finally:
        time.sleep(60)