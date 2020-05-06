import pyb
import time

def flash_led():
    print('Flashing LEDs. Ctrl-C to quit.')
    led1 = pyb.LED(1)
    while(True):
        #pyb.LED(1).on()
        led1.toggle()
        #pyb.delay(1000)
        time.sleep(1)


flash_led()