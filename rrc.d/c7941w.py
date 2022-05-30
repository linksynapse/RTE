import serial, struct

class c7941w:
	def __init__(self, Component, Baudrate):
		self.SERIAL = serial.Serial(Component, Baudrate)
		self.SERIAL.timeout = 0.1

	def GetMifare(self):
		dummy = bytearray()
		self.SERIAL.write(bytearray([0xAB,0xBA,0x00,0x10,0x00,0x10]))
		data = self.SERIAL.read(1024)
		if data[0] == 0xcd:
			if data[1] == 0xdc:
				if data[3] == 0x81:
					for x in range(5,5+data[4]):
						dummy.append(data[x])
				else:
					return 0
			else:
				return 0
		else:
			return 0

		r = struct.unpack('<L',dummy)
		return str(r[0])

	def GetEM(self):
		dummy = bytearray()
		self.SERIAL.write(bytearray([0xAB,0xBA,0x00,0x15,0x00,0x15]))
		data = self.SERIAL.read(1024)
		if data[0] == 0xcd:
			if data[1] == 0xdc:
				if data[3] == 0x81:
					for x in range(5,5+data[4]):
						dummy.append(data[x])
				else:
					return 0
			else:
				return 0
		else:
			return 0

		r = struct.unpack('>HBH',dummy)
		return (str(r[1]).zfill(3) + str(r[2]).zfill(5))