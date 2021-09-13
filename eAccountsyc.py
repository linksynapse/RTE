from module import CONF, LOG4S, API, DATA
from module import NT_SYS_PUBIP, NT_SYS_NATIP
import traceback
import time
import json

def GetAccountData(proj_id):
	data = API.DownloadUser(proj_id)
	if(data[0]):
		resultCode = data[2]
		if(resultCode == 0):
			data = data[1]
			with open('data/account.json','w',encoding='utf-8') as fs:
				json.dump(data, fs, indent="\t")

			LOG4S.info('eAccountsyc', 'Successfully gettering account information.')
		else:
			raise ValueError("Can not load account data.")
	else:
		raise ValueError("Can not access server.")

if __name__ == '__main__':
	cpu_id = None
	ipaddress = None
	macaddress = None
	gant_id = None
	gant_name = None
	proj_id = None
	serial = None
	status = None

	try:
		data = API.GetDeviceInformation("F0000002CPUID", NT_SYS_PUBIP, "00:EF:0A:24:04:01")
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
					serial = x['serial']
					status = x['status']

				LOG4S.info('eAccountsyc', 'Successfully gettering device information.')
				LOG4S.info('eAccountsyc', json.dumps(data))

				GetAccountData(proj_id=proj_id)
			else:
				raise ValueError("No record")
		else:
			raise ValueError("Can not gettering device information.");
	except Exception as err:
		LOG4S.err('eAccountsyc','Unknown error fail execute verification module\r\n' + str(type(err)) + "\r\n" + traceback.format_exc())
		time.sleep(1)