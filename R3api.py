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

		self.baseurl = "https://" + self.host + ":" + str(self.port) + "/"
		self.mdsurl = "http://" + config.mds_host() + ":" + str(config.mds_port()) + "/"
		self.cookie = None

	def GetSerialKey(self, CPUID):
		data = {
			"CPUID":CPUID
		}
		try:
			res = requests.post(self.baseurl + "g_serial", params=data, verify=False, headers=self.headers)
		except:
			return (False, "connection error", 2)
		
		if(res.status_code == 200):
			result = json.loads(res.text)
			if(result['code'] == 1):
				return (True, result['data']['SerialKey'], 1)
			else:
				return (False, result['reason'], 4)
		else:
			return (False, "connection error", 3)

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
				"time":data[2]
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

	def DownloadUser(self):
		try:
			self.headers['cookie'] = self.cookie
			res = requests.post(self.mdsurl + "user", verify=False, headers=self.headers)
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

	def CheckStatus(self):
		try:
			self.headers['cookie'] = self.cookie
			res = requests.post(self.mdsurl + "stanby_user", verify=False, headers=self.headers)
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

