import sys
import Log4s
import Config
import HAL
import Accessories
import Data

def Start(self):
	config = Config.Config("Config/sys.conf")
	Log = Log4s.Log4s(self.config)
	Aies = Accessories.Manager(self.config)
	Dao = Data.Manager(self.config)
	Reader = HAL.handler(self.config)

	Aies.PlayLoadComplate()
	try:
		self.Read()
	except KeyboardInterrupt:
		self.Log.info("HardWare","KeyboardInterrupt.")
	except Exception as err:
		self.Log.err("HardWare",str(err))
	finally:
		sys.exit()

def Read(self):
	while True:
		EM = self.Reader.GetEM()

		data = self.Dao.Verify(EM)
		if data[0]:
			# Pass
			self.Dao.CheckTime(data[1])
			self.Aies.OnBlue()
			self.Aies.FulldownExt1()
			self.Aies.PlaySuccess()
		else:
			# Deny
			self.Aies.OnRed()
			self.Aies.FulldownExt2()
			self.Aies.PlayFail()
		
		self.Aies.ClearLed()
		self.Aies.RaisingAll()
