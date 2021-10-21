from module import CONF, LOG4S, DATA
from module import RfidReader as HAL
from module import Accessories as ACSI
import sys

#def Start():
#	
#	try:
#		Read()
#	except KeyboardInterrupt:
#		LOG4S.info("HardWare","KeyboardInterrupt.")
#	except Exception as err:
#		LOG4S.err("HardWare",str(err))
#	finally:
#		sys.exit()

def Read(lock):
	Aies = ACSI.Accessories(CONF)
	Reader = HAL.RfidReader(CONF)
	
	Aies.PlayLoadComplate()
	while True:
		EM = Reader.GetEM()

		data = DATA.Verify(LOG4S,lock,EM)
		if data[0]:
			# Pass
			print(EM)
			DATA.CheckTime(LOG4S, CONF.Database(), lock, data[1])
			Aies.OnBlue()
			Aies.FulldownExt1()
			Aies.PlaySuccess()
		elif str(EM) == '0':
			continue
		else:
			# Deny
			print(EM)
			Aies.OnRed()
			Aies.FulldownExt2()
			Aies.PlayFail()
		
		Aies.ClearLed()
		Aies.RaisingAll()