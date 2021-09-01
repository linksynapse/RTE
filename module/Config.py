import configparser

class Config:
	def __init__(self, path):
		self.path = path
		self.config = configparser.ConfigParser()
		self.config.read_file(open(self.path))

	#
	# Log4sys module
	#
	#

	def error(self):
		return self.config.get('log','error_log_path')

	def warning(self):
		return self.config.get('log','warning_log_path')

	def information(self):
		return self.config.get('log','information_log_path')

	def level(self):
		return int(self.config.get('log','print_log_level'))

	def echo(self):
		return int(self.config.get('log','echo_log_level'))

	#
	# R3api module
	#
	#

	def api_host(self):
		return self.config.get('APIinterface','host')

	def api_port(self):
		return int(self.config.get('APIinterface','port'))

	def mds_host(self):
		return self.config.get('network','mds_address')

	def mds_port(self):
		return int(self.config.get('network','mds_port'))

	def license(self):
		return self.config.get('system','license_key')

	def serialkey(self):
		return self.config.get('system','serial_key')

	def wserialkey(self, key):
		self.config.set('system','serial_key', key)
		with open(self.path, 'w') as configfile:
			return self.config.write(configfile)

	def token(self):
		return self.config.get('system','token')

	def wtoken(self, key):
		self.config.set('system','token', key)
		with open(self.path, 'w') as configfile:
			return self.config.write(configfile)

	def version(self):
		return self.config.get('system','version')

	def Component(self):
		return self.config.get('hardware','component')

	def Baudrate(self):
		return int(self.config.get('hardware','baudrate'))

	def Database(self):
		return self.config.get('data','database_path')

	def LedRed(self):
		return int(self.config.get('pin','led_red'))

	def LedGreen(self):
		return int(self.config.get('pin','led_green'))

	def Buzzer(self):
		return int(self.config.get('pin','buzzer'))

	def LedBlue(self):
		return int(self.config.get('pin','led_blue'))

	def ExtPin1(self):
		return int(self.config.get('pin','ext1'))

	def ExtPin2(self):
		return int(self.config.get('pin','ext2'))
