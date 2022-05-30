import logging
import json
import requests

class rda(object):
    def __init__(self, host):
        self.headers = {
							'Content-Type': 'application/json', 
							'Accept': 'application/json', 
							'contentType': 'application/json; charset=UTF-8', 
							'mimeType': 'application/json'
						}

        self.baseurl = 'http://' + host + '/'
        self.cookie = None

    def GetDataFromJsonByPOST(self, url, data):
        try:
            self.headers['cookie'] = self.cookie
            res = requests.post(self.baseurl + url, json=data, verify=False, headers=self.headers)
        except:
            return {
                "result" : False,
                "msg" : "Cannot connect to server. check your internet status.",
                "code" : 2
            }
			
        if(res.status_code == 200):
            result = json.loads(res.text)
            if(result['Result'] == 0):
                return {
                "result" : True,
                "msg" : result['Data'],
                "code" : 0
            }
            else:
                return {
                "result" : False,
                "msg" : result['Data'][0]['Message'],
                "code" : result['Data'][0]['MsgCode']
            }
        else:
            return {
                "result" : False,
                "msg" : "Received invalid return code from server. check your data.",
                "code" : 3
            }

    def UploadHistory(self, gant_id, gant_name, serial, proj_id, proj_name, status, data):
        r = self.GetDataFromJsonByPOST('C8CDC5F3D46143B664D72D039B5832FC', {
			"gant_id":gant_id,
			"gant_name":gant_name,
			"serial":serial,
			"proj_id":proj_id,
			"proj_name":proj_name,
			"status":status,
			"data":data
		})

        if r['result']:
            logging.info('History upload successful to server. return code -> %d' %r['code'])
            return True, r['msg']
        else:
            logging.error('%s return code -> %d' ,r['msg'] ,r['code'])
            return False, None

    def DownloadDeviceInform(self, cpu_id, nataddr, macaddress, cpu_usage, disk_usage, temp, ram_usage, wifi_ssid, wifi_quality):
        r = self.GetDataFromJsonByPOST('4CF2C6704161CB5C3DCB0FFE9A52B4EC', {
            "cpu_id" : cpu_id,
            "nataddr" : nataddr,
            "macaddr" : macaddress,
            "cpu_usage" : cpu_usage,
            "disk_usage" : disk_usage,
            "temp" : temp,
            "ram_usage" : ram_usage,
            "wifi_ssid" : wifi_ssid,
            "wifi_quality" : wifi_quality
        })

        if r['result']:
            logging.info('Device information download successful from server. return code -> %d' ,r['code'])
            return True, r['msg']
        else:
            logging.error('%s return code -> %d' ,r['msg'] ,r['code'])
            return False, None