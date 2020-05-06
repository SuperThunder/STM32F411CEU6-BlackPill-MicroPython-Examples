## Dependencies (for ubuntu 18.04):
- git
- gcc
- make
- gcc-arm-none-eabi
- libnewlib-arm-none-eabi on **Ubuntu 18.04**



## Build process (from WeAct)
### 1) Make MicroPython cross compiler
    git clone https://github.com/micropython/micropython.git
    cd micropython
    git submodule update --init
    cd mpy-cross
    make -j4

### 2) Make MicroPython firmware image for the F411 board
    cd ../ports/stm32/boards
    git clone https://github.com/mcauser/WEACT_F411CEU6

    cd ..

    make BOARD=WEACT_F411CEU6 -j4

- I used the mcauser repository, you can also use the WeAct repository

### 3) Retrieve build artifacts
    cd build-WeAct_F411CE/

Where you can find

    firmware.dfu
    firmware.elf
    firmware.hex
    firmware.map
    firmware0.bin
    firmware1.bin

Firmware 0 and 1 must be flashed contiguously.


### Optional: Enable external flash
If you have soldered an SPI flash chip to the underside of the board, or connected one to the pins, you can have MicroPython use that as storage instead of the integrated flash. In both cases, the pins A4 (CS), A5 (SCK), A6 (MISO), and A7 (MOSI) are now in use for SPI.

External SPI flash **enabled**:

    #define MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE (0)

in mpconfigboard.h. See [here](https://github.com/mcauser/WEACT_F411CEU6#flash) for details on setting the defined flash chip size (eg 32Mbit, 64Mbit).

## Flashing Process
You have a few options in how to upload the firmware.
In all cases, you will want to put the board into programming mode by
1. Hold NRST button
2. Hold BOOT0 button
3. Release NRST
4. Release BOOT0

Then you can flash the board:

### 1) By DFU (with STM32CubeProgrammer)
- You can also use dfu-util as described in the mcauser repo
- Oddly, STM32CubeProgrammer does not accept .dfu files, but you can use the .hex or .elf
### 2) By ST-LINK
- Connect the ST-Link to the board. Remember not to plug the 3v3 pin in if you are powering the board by USB, or will be plugging USB in later.

### 3) By Serial
- Connect the board to a serial adapter and use STM32CubeProgrammer or st-flash to upload the firmware


## Serial REPL and 'USB drive' of Python files
After flashing, press the NRST button to reboot the board. 

It should now show up as a ~40KB mass storage device and a COM serial port device when plugged into your PC by USB. The serial port can be connected to at 115200 bps.