import time
import _thread
import sys

msgQuitLEDBlink = 0

print('Hello world! I can count to 10:')
for i in range(1,11):
    print(i*i)


def flash_led():
    print('Flashing LEDs')
    led1 = pyb.LED(1)
    while(True):
        if(msgQuitLEDBlink==1):
            _thread.exit()
        #pyb.LED(1).on()
        led1.toggle()
        #pyb.delay(1000)
        time.sleep(1)

# Start the LED blink thread
_thread.start_new_thread(flash_led, ())
time.sleep(0.1)

while(True):
    text = input('\nEnter text: ')
    print("entered: " + text)

    if(text=="quit"):
        msgQuitLEDBlink=1
        sys.exit()