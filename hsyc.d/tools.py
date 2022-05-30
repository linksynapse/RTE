from requests import get
from getmac import get_mac_address as gma
import socket
import os
import psutil

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

def GetWIFIQuality():
    result = os.popen("iwconfig wlan0 | grep Link | awk '{$1=$1;print}'").read().replace('\n', '').split()[1]
    return result

def GetWIFISSID():
    result = os.popen("iwconfig wlan0 | grep ESSID | awk '{$1=$1;print}'").read().replace('\n', '').split()[3].split(':')[1].replace('"','')
    return result

def GetDiskUsage():
    st = os.statvfs("/")

    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    free = st.f_bavail * st.f_frsize

    return round(used / total * 100,2)

def GetCPUUsage():
    return psutil.cpu_percent()

def GetRamUsage():
    return psutil.virtual_memory().percent

def GetTemp():
	temp = os.popen("vcgencmd measure_temp").readline()
	result = temp.replace("temp=","").replace("'C", "").replace('\n', '')
	return result