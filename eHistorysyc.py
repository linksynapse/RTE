import Config
import Log4s
import R3api
import SyS
import traceback
import time
import Data

if __name__ == '__main__':
	config = Config.Config("Config/sys.conf")
	log = Log4s.Log4s(config)
	r3api = R3api.R3api(config)
	d = Data.Manager(config)
	serialkey = None

	try:
		data = r3api.GetSerialKey(SyS.GetCPUID())
		# Successfully getting serialkey from authentication server
		if(data[0]):
			serialkey = data[1]
			# Save serialkey
			config.wserialkey(data[1])
			log.info('Authentication', '[0x8000200' + str(data[2]) + '] Serialkey validation succeeded')
			data = r3api.VerifyLicense()
			if(data[0]):
				# Save token
				log.info('Authentication', '[0x8000100' + str(data[2]) + '] license validation succeeded')
				config.wtoken(data[1])
				log.info('Authentication', '[0x8000300' + str(data[2]) + '] Access token initalize successful')

				# Collecting device infomation
				data = {
					"SerialKey":config.serialkey(),
					"Token":config.token(),
					"PublicAddress":SyS.GetPublicIPaddress(),
					"NATAddress":SyS.GetNATIPaddress(),
					"HostName":SyS.GetHostName(),
					"Version":config.version()
				}
				data = r3api.ApplyTokenToServer(data)

				if(data[0]):
					while(True):
						temp = d.SelectHistory()
						if(temp[0]):
							result = temp[1] + (serialkey,0)
							data = r3api.UploadHistory(result)
							if(data[0]):
								log.info('IO_History', '[0x8000600' + str(data[2]) + '] ' + data[1])
								d.DoneSendHistory(temp[1])
							else:
								log.err('IO_History', '[0x8000600' + str(data[2]) + '] ' + data[1])
						else:
							log.info('IO_History', '[0x80000000] Waiting input history file')
							time.sleep(10)
				else:
					log.err('Authentication', '[0x8000400' + str(data[2]) + '] ' + data[1])
			else:
				# License wrong still continue execute local
				log.err('Authentication', '[0x8000100' + str(data[2]) + '] ' + data[1])
		else:
			# Serialnumber was wrong stop service device
			log.err('Authentication','[0x8000200' + str(data[2]) + '] ' + data[1])
	except Exception as err:
		log.err('Authentication','[0x8000F000] Unknown error fail execute verification module\r\n' + str(type(err)) + "\r\n" + traceback.format_exc())
		time.sleep(60)