import Config
import Log4s
import R3api
import SyS
import traceback
import time
import Data
import json

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
						data = r3api.CheckStatus({'serialkey':serialkey})
						if(data[1]['Update'] == 1):
							data = r3api.DownloadUser()
							if(data[0]):
								log.info('IO_Users', '[0x8000700' + str(data[2]) + '] Starting writing user to client count -> ' + str(len(data[1])))
								with open('data/account.json','w',encoding='utf-8') as fs:
									json.dump(data[1], fs, indent="\t")

								data = r3api.ProgressWork({'serialkey':serialkey,"prog":100})
								data = r3api.ChangeStatus({'serialkey':serialkey,"Status":3})
								log.info('IO_Users', '[0x80007001] Ended download user from server')
							else:
								log.err('IO_Users', '[0x8000700' + str(data[2]) + '] ' + data[1])

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