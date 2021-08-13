import sys
import Log4s
import Config
import HAL
import Accessories
import Data

class tMain:
	def __init__(self):
		self.config = Config.Config("Config/sys.conf")
		self.Log = Log4s.Log4s(self.config)
		self.Aies = Accessories.Manager(self.config)
		self.Dao = Data.Manager(self.config)
		self.Reader = HAL.handler(self.config)

	def Start(self):
		self.Aies.PlayLoadComplate()
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
			Mifare = self.Reader.GetMifare()
			EM = self.Reader.GetEM()

			if Mifare != 0:
				data = self.Dao.Verify(Mifare)
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
			elif EM != 0:
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
			else:
				pass

			self.Aies.ClearLed()
			self.Aies.RaisingAll()


if __name__ == '__main__':
	worker = tMain()
	worker.Start()
