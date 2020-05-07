# USE:
# Copy this file (as main.py), FourDigitSevenSegmentShift_Timer.py, and ShiftRegister.py to your board

# COMPONENTS:
# 1x STM32F411CEU6
# 2x 74HC595N
# 1x 16 pin common-anode 4 digit 7 segment display (YSD-439AK2B-35)

# PINS:
# A3->SER of first shift register
# A2->RCLK of all shift registers
# A1->SRCLK of all shift registers

# Shift registers: SRCLR <- Vcc,  OE <- GND    
# 3.3v to SR Vcc, GND TO GND
# Link Qh' of previous SR to SER of next one
# SR output pin connections to 4 digit 7 seg display described in the class

# Remember to use resistors between the digit cathode pins and the display pin
# (or, a resistor after all the anode pins of the display)


# Implementeed but not tested: colon and high-dot functionality

# TODO: deinit timer on exit

import ShiftRegister
import FourDigitSevenSegmentShift_Timer

import micropython
# Very useful for debugging timer callback code that doesn't work
# Allows full traceback messages to be displayed
micropython.alloc_emergency_exception_buf(1000)

def main():
    print("Shift Register + 4digit7segment with Timer")

    sr = ShiftRegister.ShiftRegister('PA3', 'PA1', 'PA2', chain=2)
    display = FourDigitSevenSegmentShift_Timer.FourDigitSevenSegmentShift(sr, clkHz=1000)

    #for i in range(0, 10):
        #display.show(str(i)*4)
        #time.sleep(0.5)

    # non-latin characters work too :)
    #display.show(digits="三"*4)

    while(True):
        digits = input("Enter 4 digits to display: ")
        display.show(digits)


main()