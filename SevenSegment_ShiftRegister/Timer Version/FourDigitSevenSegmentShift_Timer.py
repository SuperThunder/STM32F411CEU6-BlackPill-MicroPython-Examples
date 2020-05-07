# Implementation of a shift register with a timer to multiplex the LEDs
# TODO: deinit

import pyb
import time

class FourDigitSevenSegmentShift:
    def show(self, digits):
        if(len(digits) != 4):
            print("Must send 4 digits")
            return -1

        self.DIGITS = digits
        self.precomputeDigitBytes()


    # Precomputes all digits' data and control bytes to eliminate function calls by timer interrupt handler
    def precomputeDigitBytes(self):
        for i in range(0, 4):
            # Data byte
            self.SR_DATA_ALL[i*2+0] = self.getSevenSegmentDigitByte(self.DIGITS[i], DP=False)
            # Control byte
            self.SR_DATA_ALL[i*2+1] = self.getSevenSegmentControlByte(i, colon=False, highdot=False)


    # return 7 seg byte representation (if possible) for char
    # represents digit as a byte of on/off for A B C D E F G DP
    # byte place for segment:                  7 6 5 4 3 2 1 0                                          
    # (DP = decimal point)
    #     A A A
    #   F       B
    #   F       B
    #   F       B
    #     G G G
    #   E       C
    #   E       C
    #   E       C
    #     D D D      (DP)
    #   
    #
    def getSevenSegmentDigitByte(self, digit, DP=False ):
        # TODO: Letter/char mappings too
        # As the display is common anode, we put a 1 on bits we DON'T want to see
        # As then the shift register will put out a 1 and not sink any current for that segment
        # So 0 shows all segments and 255 turns all off (including DP)
        mappings = {
            0: 2,
            1: 159,
            2: 36,
            3: 12,
            4: 152,
            5: 72,
            6: 64,
            7: 30,
            8: 0,
            9: 8,
            '0': 2,
            '1': 159,
            '2': 36,
            '3': 12,
            '4': 152,
            '5': 72,
            '6': 64,
            '7': 30,
            '8': 0,
            '9': 8,
            '三': 108
        }

        if( digit in mappings.keys() ):
            segmentbyte = mappings[digit]
        else:
            # show the three horizontal lines to indicate unmapped input
            segmentbyte = mappings['三']

        if( DP == True ):
            # Set 1s column bit ON by AND with 1111 1110
            # (as 0 in segment bit means on)
            segmentbyte &= 254
        else:
            # Set 1s column bit OFF by OR with 0000 0001
            segmentbyte |= 1
            
        return segmentbyte

    # This byte controls the cathodes for each digit (1 to 4)
    # and also the colon in the 2nd column and high dot in 3rd column
    # Byte to 2nd shift register pins:
    #   7   6   5   4   3   2   1   0
    #   A   B   C   D   E   F   G   H
    #   dt  cl  X   D4  D3  D2  D1  X
    def getSevenSegmentControlByte(self, activedigit, colon=False, highdot=False ):
        controlbyte = 0

        # The digit are + so send 1 to turn on
        # activedigit is the digit # that we want turned on
        controlbyte |= (1 << (activedigit+1) )

        if(colon):
            controlbyte |= 64

        if(highdot):
            controlbyte |= 128
        
        return controlbyte


    # Show list of 4 provided digits (Multiplexed)
    # and also the colon/high dot
    # As this method is an interrupt handler, it cannot allocate anything on the heap, nor can any function that it calls!
    def FourDigitSevenSegmentShiftDisplay_Timer(self, timer):
        #print("Digits: " + self.DIGITS)

        # reset back to first digit
        if(self.CurrentDigit == 4):
            self.CurrentDigit = 0

        # Assemble 2 byte data/digit select sequence
        #data = bytearray(2)
        #self.SR_DATA[0] = self.getSevenSegmentDigitByte(self.DIGITS[self.CurrentDigit], DP=False)
        #self.SR_DATA[1] = self.getSevenSegmentControlByte(self.CurrentDigit, colon, highdot)

        # To avoid function calls in this interrupt handler, we have all the data/control bytes for each digit-precomputed already
        self.SR_DATA[0] = self.SR_DATA_ALL[self.CurrentDigit*2+0]
        self.SR_DATA[1] = self.SR_DATA_ALL[self.CurrentDigit*2+1]
        
        # Send sequence to shift registers
        self.SR.shiftOut(self.SR_DATA)

        # Display next digit on next run
        self.CurrentDigit += 1

    def __init__(self, shiftreg, clkHz = 1000):
        self.SR = shiftreg
        self.SR_DATA = bytearray(2)
        self.SR_DATA_ALL = bytearray(8)
        self.DIGITS = "0000" # currently displayed digits stored here
        self.show("8888")

        self.CurrentDigit = 0

        # 1 khz by default
        self.DisplayTimer = pyb.Timer(1, freq=clkHz)
        #self.DisplayTimer.callback(lambda x: self.FourDigitSevenSegmentShiftDisplay() )
        self.DisplayTimer.callback( self.FourDigitSevenSegmentShiftDisplay_Timer )