import pyb

class TestClassTimerCallback:
	def __init__(self):
		self.t2 = pyb.Timer(2, freq=3)
		self.t2.callback( self.toggleLED )
	
	def toggleLED( timer ):
		pyb.LED(1).toggle()


def test():
	t = TestClassTimerCallback()

test()