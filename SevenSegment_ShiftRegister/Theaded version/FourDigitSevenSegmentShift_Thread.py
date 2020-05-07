# Implementation of a shift register with a thread to multiplex the 

import _thread
import time



class FourDigitSevenSegmentShift:
    def __init__(self, shiftreg, clkHz = 1000):
        self.SR = shiftreg
        self.DIGITS = "0000" # display thread checks this variable

        self.clk_period_seconds = 1 / clkHz

        # TODO: probably better performance and less oddity to do this with timed interrupts
        # or create some kind of _thread wrapper that automatically makes a global var for the thread to check to indicate it should terminate
        _thread.start_new_thread(self.FourDigitSevenSegmentShiftDisplay, ())


    def show(self, digits):
        if(len(digits) != 4):
            print("Must send 4 digits")
            return -1

        self.DIGITS = digits
        #self.FourDigitSevenSegmentShiftDisplay(digits)

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


    # Show list of 4 provided digits
    # and also the colon/high dot
    def FourDigitSevenSegmentShiftDisplay(self, colon=False, highdot=False):
        #print("Digits: " + self.DIGITS)
        # multiplex between the 4 digits
        while(True):
            for i in range(0,4):
                data = bytearray(2)
                data[0] = self.getSevenSegmentDigitByte(self.DIGITS[i], DP=False)
                data[1] = self.getSevenSegmentControlByte(i, colon, highdot)
                
                self.SR.shiftOut(data)

                time.sleep(self.clk_period_seconds)