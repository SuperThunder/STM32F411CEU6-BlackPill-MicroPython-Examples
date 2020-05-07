import pyb

# class for 74hc595n
# (chain of one or more)
class ShiftRegister:
    def __init__(self, dataPin, clkPin, latchPin, chain=1):
        Pin = pyb.Pin        
        # init pins
        self.datapin = Pin(dataPin, Pin.OUT)
        self.clkpin = Pin(clkPin, Pin.OUT)
        self.latchpin = Pin(latchPin, Pin.OUT)
        self.datapin.value(0)
        self.clkpin.value(0)
        self.latchpin.value(0)

        self.chainlength = chain
        

        
    # Shift out by writing on data line and sending clock
    # data should be a byte array equal to the S.R. chain length
    def shiftOut(self, data):
        # ground latchpin while transmitting (thx arduino docs)
        self.latchpin.off()

        if(len(data) != self.chainlength):
            print("Data array of length {cl} does not match specified shift register chain length of {srcl}".format(cl=len(data), srcl=self.chainlength))
            return None

        # NOT ALLOWED WITH TIMER INTERRUPTS:
        # for byte in reversed(data)
        # as we are allocating memory for the reversed() and for the 'for x in y' iterator

        # loop for each byte we want to send
        # send lower bytes first so that array order results in same order
        # in the chain of shift registers
        for i in range(self.chainlength, 0, -1):
            # send the byte's bits out
            byte = data[i-1]
            for bit in range(0,8):
                # get bit from data byte
                # send bits in order 0 1 2 3 4 5 6 7
                b = (byte >> bit) & 1
                
                # send bit on data line
                self.datapin.value(b)

                # send clock pulse
                self.clkpin.value(1)
                self.clkpin.value(0)

        # activate storage->output latch
        self.latchpin.on()