from module import CONF, LOG4S, API, DATA
from module import NT_SYS_PUBIP, NT_SYS_NATIP, NT_SYS_CPUID, NT_SYS_MACAR
import traceback
import time
import json

def SendHistory(gant_id, gant_name, serial, proj_id, proj_name, status, lock):
	data = DATA.SelectHistory(LOG4S, CONF.Database(), lock)[1]
	data = json.loads(data)
	if(len(data) > 0):
		resultCode = API.UploadHistory(gant_id=gant_id, gant_name=gant_name,serial=serial,proj_id=proj_id,proj_name=proj_name,status=status,data=data)[2]

		if(resultCode == 0):
			LOG4S.info('eHistorysyc', 'Successfully uploading history.')
			for x in data:
				DATA.ChangeStatus(LOG4S, CONF.Database(), lock, x)
		else:
			LOG4S.err('eHistorysyc', 'Fail uploading history')
	else:
		LOG4S.info('eHistorysyc', 'No record history.')

def eHistorysycExec(lock):
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

				LOG4S.info('eHistorysyc', 'Successfully gettering device information.')
				LOG4S.info('eHistorysyc', json.dumps(data))

				SendHistory(proj_id=proj_id,proj_name=proj_name,gant_name=gant_name,gant_id=gant_id,status=status,serial=serial,lock=lock)
			else:
				raise ValueError("No record")
		else:
			raise ValueError("Can not gettering device information.");
	except Exception as err:
		LOG4S.err('eHistorysyc','Unknown error fail execute verification module\r\n' + str(type(err)) + "\r\n" + traceback.format_exc())
		time.sleep(1)