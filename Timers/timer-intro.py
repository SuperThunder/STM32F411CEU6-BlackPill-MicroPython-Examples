# MicroPython pyb doc on Timers:
# https://docs.micropython.org/en/latest/library/pyb.Timer.html#pyb-timer


# WeAct MicroPython library doc:
# https://github.com/WeActTC/MiniF4-STM32F4x1/blob/master/General%20document/MicroPython%E9%83%A8%E5%88%86%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B%20_WeAct%E5%B7%A5%E4%BD%9C%E5%AE%A4.pdf



from pyb import Timer
import time


# F411CE TIMER MAX SPEEDS:
# 96MHz: Timers 1, 9, 10, 11
# 48MHz: Timers 2, 3, 4, 5

# main.py -- put your code here!
def main():
    # 2 Hz timer
    # Timer( Timer#, freq )
    TIM1 = Timer(1, freq=2)

    # get/set frequency (of your timer instance)
    # this is probably what you want to set
    # TIM1.freq(5)
    # Can set non-integer frequencies too!
    # TIM1.freq(0.3)
    # TIM1.freq(1.5)

    # Set callback function run on each counter tick:
    # TIM1.callback(lambda t: pyb.LED(1).toggle)
    # TIM1.callback( lambda x: your_function() )

    # Timer callback functions need to have a parameter to accept the timer if you want to set them as the callback without a lambda
    # eg:
    # TIM1.callback( do_stuff )
    #
    # requires:
    # def do_stuff( timer ):
    #   ...do something...
    #
    # def do_stuff():
    # .....
    # will not work!


    # Clear callback:
    # TIM1.callback(None)

    # delete timer, callback, and any channel callbacks
    # TIM1.deinit()
    # or even 
    # Timer(1).deinit()
    

    # 2Hz led flash
    TIM1.callback( lambda x: toggleLED1() )


    # Timers can be useful for flashing periodic/recurring tasks
    # eg PWM, flashing an LED, multiplexing between LEDs



def timer_advanced():
    # get actual frequency of the timer
    # TIM1.source_freq()
    # ^ 96000000 (96MHz)

    # Timer Modes
    # ARR: Auto Reload Register ('defines the end of pulse')
    # Up: Counts 0 to ARR (default)
    # Down: Counts ARR to 0
    # Center: 0 to ARR to 0

    # get/set prescaler (clock frequency divider) value
    # bigger prescaler means less frequent timer
    # TIM1.prescaler()
    # TIM1.prescaler(1)

    # get/set period in TIMER CLOCK CYCLES
    # TIM1.period(200)

    # Update frequency  = (TIMER_CLOCK) / ( Prescaler + 1 ) / (Period+1)

    # get counter value
    # TIM1.counter()

    # Timer Channels
    # see https://docs.micropython.org/en/latest/library/pyb.Timer.html#pyb.Timer.channel
    # 'Each channel can be configured to perform pwm, output compare, or input capture. 
    #  All channels share the same underlying timer, which means that they share the same timer clock.'
    #  
    # While they share the same timer clock, they have different counters and can perform different functions
    # eg. different pwm pulse widths on different channels
    pass



def toggleLED1():
    led1 = pyb.LED(1)
    led1.toggle()



main()
