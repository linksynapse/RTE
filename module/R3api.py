import json
import requests

class R3api(object):
	def __init__(self, config):
		self.host = config.api_host()
		self.port = config.api_port()
		self.config = config

		self.headers = {
							'Content-Type': 'application/json', 
							'Accept': 'application/json', 
							'contentType': 'application/json; charset=UTF-8', 
							'mimeType': 'application/json'
						}

		self.baseurl = "http://" + self.host + ":" + str(self.port) + "/"
		self.mdsurl = "http://" + config.mds_host() + ":" + str(config.mds_port()) + "/"
		self.cookie = None

	def GetDeviceInformation(self, cpu_id, nataddr, pubaddr, macaddress):
		data = {
			"cpu_id":cpu_id,
			"pubaddr":pubaddr,
			"nataddr":nataddr,
			"macaddr":macaddress
		}
		try:
			res = requests.post(self.baseurl + "4CF2C6704161CB5C3DCB0FFE9A52B4EC", json=data, verify=False, headers=self.headers)
		except:
			return (False, "connection error", 2)
		
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['Result'] == 0):
				return (True, result['Data'], 0)
			else:
				return (False, result['Data'][0]['Message'], result['Data'][0]['MsgCode'])
		else:
			return (False, "connection error", 3)

	# 
	#	Unused system
	#
	def VerifyLicense(self):
		data = {
			"SERIALKEY":self.config.serialkey(),
			"LICENSE":self.config.license()
		}
		try:
			res = requests.post(self.baseurl + "g_token", params=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['data']['token'], 1)
			else:
				return (False, result['reason'], 5)
		else:
			return (False, "Error from server", 3)

	# 
	#	Unused system
	#
	def ApplyTokenToServer(self, data):
		try:
			res = requests.post(self.baseurl + "s_info", params=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['reason'], 1)
			else:
				return (False, result['reason'], 0)
		else:
			return (False, "Error from server", 3)


	# 
	#	Unused system
	#
	def Authentification(self, data):
		try:
			res = requests.post(self.mdsurl + "g_session", params=data, verify=False, headers=self.headers)
			self.cookie = res.headers.get('Set-Cookie')
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			print(result)
			if(result['code'] == 1):
				return (True, result['reason'], 1)
			else:
				return (False, result['reason'], result['code'])
		else:
			return (False, "Error from server", 3)

	
	def UploadHistory(self, data):
		try:
			data = {
				"badge":data[0],
				"card":data[1],
				"time":data[2],
				"serialkey":data[4]
			}
			self.headers['cookie'] = self.cookie
			res = requests.post(self.mdsurl + "history", params=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['reason'], 1)
			else:
				return (False, result['reason'], result['code'])
		else:
			return (False, "Error from server", 3)

	def DownloadUser(self, proj_id):
		try:
			data = {
				'proj_id' : proj_id
			}

			self.headers['cookie'] = self.cookie
			res = requests.post(self.baseurl + "57C5A9EEA786CD47EE17D720420493FA", json=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['Result'] == 0):
				return (True, result['Data'], 0)
			else:
				return (False, result['Data'][0]['Message'], result['Data'][0]['MsgCode'])
		else:
			return (False, "connection error", 3)

	# 
	#	Unused system
	#
	def ProgressWork(self, data):
		try:
			self.headers['cookie'] = self.cookie
			res = requests.post(self.mdsurl + "prog", params=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['data'], 1)
			else:
				return (False, result['reason'], result['code'])
		else:
			return (False, "Error from server", 3)

	# 
	#	Unused system
	#
	def CheckStatus(self,data):
		try:
			self.headers['cookie'] = self.cookie
			res = requests.post(self.mdsurl + "stanby_user", params=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['data'], 1)
			else:
				return (False, result['reason'], result['code'])
		else:
			return (False, "Error from server", 3)

	# 
	#	Unused system
	#
	def ChangeStatus(self, data):
		try:
			self.headers['cookie'] = self.cookie
			res = requests.post(self.mdsurl + "do_user", params=data, verify=False, headers=self.headers)
		except:
			return (False, "Error from server", 2)
			
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['data'], 1)
			else:
				return (False, result['reason'], result['code'])
		else:
			return (False, "Error from server", 3)

