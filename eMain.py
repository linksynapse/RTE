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

	try:
		data = r3api.GetSerialKey(SyS.GetCPUID())
		# Successfully getting serialkey from authentication server
		if(data[0]):
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
					log.info('Authentication', '[0x8000400' + str(data[2]) + '] ' + data[1])
					data = {
						"token":config.token()
					}
					data = r3api.Authentification(data)
					if(data[0]):
						log.info('Authentication', '[0x8000500' + str(data[2]) + '] ' + data[1])

						while(True):
							temp = d.SelectHistory()
							if(temp[0]):
								data = r3api.UploadHistory(temp[1])
								if(data[0]):
									log.info('IO_History', '[0x8000600' + str(data[2]) + '] ' + data[1])
									d.DoneSendHistory(temp[1])
								else:
									log.err('IO_History', '[0x8000600' + str(data[2]) + '] ' + data[1])

							data = r3api.CheckStatus()
							if(data[1]['Update'] == 1):

								
								data = r3api.DownloadUser()
								if(data[0]):
									log.info('IO_Users', '[0x8000700' + str(data[2]) + '] Starting download user from server count -> ' + str(len(data[1])))
									d.ClearAccount()
								else:
									log.err('IO_Users', '[0x8000700' + str(data[2]) + '] ' + data[1])
								users = data[1]
								max = len(data[1]) + 1

								data = r3api.ChangeStatus({"Status":2})
								temp = 0
								for x in range(1, max):
									if(users[x - 1]['CardNumber'] != None):
										data = d.InsertAccount(users[x - 1])
									if(temp != int((x/max * 100))):
										if(data[0]):
											temp = int((x/max * 100))
											data = r3api.ProgressWork({"prog":temp})
											if(data[0] == False):
												log.warn('DO_Progress', '[0x80008000] might not apply progress. server response error code.')
										else:
											#error
											print("error")

								data = r3api.ProgressWork({"prog":100})
								data = r3api.ChangeStatus({"Status":3})
								log.info('IO_Users', '[0x80007001] Ended download user from server')

							time.sleep(1)

					else:
						log.err('Authentication', '[0x8000500' + str(data[2]) + '] ' + str(data[1]))
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