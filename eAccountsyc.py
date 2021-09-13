from module import CONF, LOG4S, API
from module import NT_SYS_PUBIP, NT_SYS_NATIP, NT_SYS_CPUID, NT_SYS_MACAR
import traceback
import time
import json

def GetAccountData(lock, proj_id):
	data = API.DownloadUser(proj_id)
	if(data[0]):
		resultCode = data[2]
		if(resultCode == 0):
			data = data[1]
			try:
				lock.acquire()
				with open('data/account.json','w',encoding='utf-8') as fs:
					json.dump(data, fs, indent="\t")
			except Exception as err:
				LOG4S.err('eAccountsyc', 'Error Download Account data.\r\n' + str(type(err)) + "\r\n" + traceback.format_exc())
			finally:
				lock.release()

			LOG4S.info('eAccountsyc', 'Successfully gettering account information.')
		else:
			raise ValueError("Can not load account data.")
	else:
		raise ValueError("Can not access server.")

def eAccountsycExec(lock):
	cpu_id = None
	ipaddress = None
	macaddress = None
	gant_id = None
	gant_name = None
	proj_id = None
	proj_name = None
	serial = None
	status = None

	try:
		data = API.GetDeviceInformation(NT_SYS_CPUID, NT_SYS_NATIP, NT_SYS_PUBIP, NT_SYS_MACAR)
		# Successfully getting serialkey from authentication server
		if(data[0]):
			resultCode = data[2]
			if(resultCode == 0):
				data = data[1]
				for x in data:
					cpu_id = x['cpu_id']
					gant_id = x['gant_id']
					gant_name = x['gant_name']
					proj_id = x['proj_id']
					proj_name = x['proj_name']
					serial = x['serial']
					status = x['status']

				LOG4S.info('eAccountsyc', 'Successfully gettering device information.')
				LOG4S.info('eAccountsyc', json.dumps(data))

				GetAccountData(proj_id=proj_id, lock=lock)
			else:
				raise ValueError("No record")
		else:
			raise ValueError("Can not gettering device information.");
	except Exception as err:
		LOG4S.err('eAccountsyc','Unknown error fail execute verification module\r\n' + str(type(err)) + "\r\n" + traceback.format_exc())
		time.sleep(1)