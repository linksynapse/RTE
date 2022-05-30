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

if __name__ == '__main__':
    print(GetCPUID())