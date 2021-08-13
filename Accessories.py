import RPi.GPIO as GPIO
import time

class Manager:
	def __init__(self,config):
		self.R = config.LedRed()
		self.G = config.LedGreen()
		self.B = config.LedBlue()
		self.Sound = config.Buzzer()
		self.Ext1 = config.ExtPin1()
		self.Ext2 = config.ExtPin2()

		# True - Nomal VCC, False - Nomal GND
		self.CloseType = True
		self.OnType = not self.CloseType

		# Initalize LED
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.R, GPIO.OUT)
		GPIO.setup(self.G, GPIO.OUT)
		GPIO.setup(self.B, GPIO.OUT)
		GPIO.setup(self.Ext1, GPIO.OUT)
		GPIO.setup(self.Ext2, GPIO.OUT)

		# Clear LED
		self.ClearLed()

		# Initalize Buzzer
		GPIO.setup(self.Sound, GPIO.OUT)

		# Cleard Buzzer
		self.OffBuzzer()

	def __del__(self):
		GPIO.cleanup()

	#
	#
	#	LED Manager
	#
	#

	def OnRed(self):
		GPIO.output(self.R, self.OnType)

	def OnGreen(self):
		GPIO.output(self.G, self.OnType)

	def OnBlue(self):
		GPIO.output(self.B, self.OnType)

	def OffRed(self):
		GPIO.output(self.R, self.CloseType)

	def OffGreen(self):
		GPIO.output(self.G, self.CloseType)

	def OffBlue(self):
		GPIO.output(self.B, self.CloseType)

	def ClearLed(self):
		self.OffRed()
		self.OffGreen()
		self.OffBlue()

	#
	#
	#	Buzzer Manager
	#
	#

	def OnBuzzer(self):
		GPIO.output(self.Sound, True)

	def OffBuzzer(self):
		GPIO.output(self.Sound, False)

	def PlayLoadComplate(self):
		scale = [261, 294, 329, 349, 392, 440, 493, 523]
		self.OnBuzzer()
		P = GPIO.PWM(self.Sound, 261)
		P.start(100)
		P.ChangeDutyCycle(10)

		for x in scale:
			P.ChangeFrequency(x)
			time.sleep(0.2)

		P.stop()
		self.OffBuzzer()


	def PlaySuccess(self):
		scale = [261, 329, 523]
		self.OnBuzzer()
		P = GPIO.PWM(self.Sound, 261)
		P.start(100)
		P.ChangeDutyCycle(10)

		for x in scale:
			P.ChangeFrequency(x)
			time.sleep(0.5)

		P.stop()
		self.OffBuzzer()

	def PlayFail(self):
		scale = [523, 261, 523, 261]
		self.OnBuzzer()
		P = GPIO.PWM(self.Sound, 523)
		P.start(100)
		P.ChangeDutyCycle(10)

		for x in scale:
			P.ChangeFrequency(x)
			time.sleep(0.4)

		P.stop()
		self.OffBuzzer()

	def PlayOtherWork(self):
		scale = [261, 523]
		self.OnBuzzer()
		P = GPIO.PWM(self.Sound, 261)
		P.start(100)
		P.ChangeDutyCycle(10)

		for x in scale:
			P.ChangeFrequency(x)
			time.sleep(0.5)

		P.stop()
		self.OffBuzzer()

	#
	#
	#	Ext 1 = Red / Ext 2 = Blue
	#
	#

	def RisingExt1(self):
		GPIO.output(self.Ext1, True)

	def FulldownExt1(self):
		GPIO.output(self.Ext1, False)

	def RisingExt2(self):
		GPIO.output(self.Ext2, True)

	def FulldownExt2(self):
		GPIO.output(self.Ext2, False)

	def RaisingAll(self):
		self.RisingExt1()
		self.RisingExt2()