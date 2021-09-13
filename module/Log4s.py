import datetime
import os

class Log4s:
	def __init__(self, config):
		self.error = config.error()
		self.warning = config.warning()
		self.information = config.information()
		self.level = config.level()
		self.echo = config.echo()


	def info(self, module, msg):
		# LEVEL 3 Enable
		if self.level > 2:
			datefolder = datetime.datetime.now().strftime('%Y%m%d')
			file = module
			AbsRootPath = self.information + "/" + datefolder
			AbsPath = AbsRootPath + "/" + file + ".log"

			if not os.path.isdir(AbsRootPath):
				os.makedirs(AbsRootPath)

			f = open(AbsPath,'a+')

			f.write("[{}] {}\r\n".format(datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f'), msg))

			if self.echo == 1:
				print("[{}] {}\r\n".format(datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f'), msg))

			f.close()

	def warn(self, module, msg):
		# LEVEL 2 Enable
		if self.level > 1:
			datefolder = datetime.datetime.now().strftime('%Y%m%d')
			file = module
			AbsRootPath = self.warning + "/" + datefolder
			AbsPath = AbsRootPath + "/" + file + ".log"

			if not os.path.isdir(AbsRootPath):
				os.makedirs(AbsRootPath)

			f = open(AbsPath,'a+')

			f.write("[{}] {}\r\n".format(datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f'), msg))
			
			if self.echo == 1:
				print("[{}] {}\r\n".format(datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f'), msg))

			f.close()

	def err(self, module, msg):
		# LEVEL 1 Enable
		if self.level > 0:
			datefolder = datetime.datetime.now().strftime('%Y/%m/%d')
			file = module
			AbsRootPath = self.error + "/" + datefolder
			AbsPath = AbsRootPath + "/" + file + ".log"

			if not os.path.isdir(AbsRootPath):
				os.makedirs(AbsRootPath)

			f = open(AbsPath,'a+')

			f.write("[{}] {}\r\n".format(datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f'), msg))
			
			if self.echo == 1:
				print("[{}] {}\r\n".format(datetime.datetime.now().strftime('%Y/%m/%dT%H:%M:%S.%f'), msg))

			f.close()