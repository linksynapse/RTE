from requests import get
from getmac import get_mac_address as gma
import socket

def GetCPUID():
	CPU_Serial = "0000000000000000"
	try:
		f = open('/proc/cpuinfo','r')
		for line in f:
			if line[0:6] == 'Serial':
				CPU_Serial = line[10:26]
		f.close()
	except:
		CPU_Serial = "ERROR00000000000"

	return CPU_Serial

def GetPublicIPaddress():
	return get('https://api.ipify.org').text


def GetNATIPaddress():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

def GetHostName():
	return socket.gethostname()

def GetMacAddress():
	return str(gma())