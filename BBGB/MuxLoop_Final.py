# Created by: Bryce Cheung
# Date: 04.06.2023
# CECS 490B Senior Project
# The Better Board Game Board

# Final Mux loop for the Rpi Pico W
# This code will control two multiplexors, one ST7735 LCD display and one rotary encoder.
# The program will first prompt the user on the LCD display to choose a game to play, once chosen
# it will send a character via UART to the rpi, and then wait for an acknowledgement back.
# Once the acknowledgement is received from the Rpi, the program will begin looping through the muxes and 32 HFX inputs.

from ST7735 import TFT
from sysfont import sysfont
from machine import ADC, SPI, Pin, UART, Timer
import time
import utime
import math

# Initializing the SPI channel for communication with the ST7735 LCD display
spi = SPI(0, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=None) # uses SPI channel 0, sck->GPIO 18, mosi(SDA)->GPIO 19
tft=TFT(spi,20,21,22) # A0(D/C)->GPIO 20, reset->GPIO 21, cs->GPIO 22
tft.initr()
tft.rgb(True)

# Init UART
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(baudrate=115200, bits=8, parity=None, stop=1)

# MUX_PINS to be initialized
# Pins 2-5 for Mux 0 | Pins 6-9 for Mux 1
MUX_PINS = [2, 3, 4, 5, 6, 7, 8, 9]
for i in MUX_PINS:
    Pin(i, Pin.OUT) # SETUP EACH PIN
    print("GPIO PIN", i, " SETUP")

# Array with positional integers so the program sends the correct Hall Effect Number to the Rpi via UART
HFX_POSITIONS0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
HFX_POSITIONS1 = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

# Init ADC PIN
Sig0 = ADC(26) # For Mux 0
Sig1 = ADC(27) # For Mux 1

def test_main():
    tft.fill(TFT.BLACK)
    tft.fillrect((0,0), (130, 30), TFT.BLUE)
    tft.text((5, 7.5), "Game Select", TFT.WHITE, sysfont, 2)
    tft.text((5, 50), "  Tic-Tac-Toe", TFT.WHITE, sysfont, 1)
    tft.text((5, 70), "  4-In-A-Row", TFT.WHITE, sysfont, 1)
    tft.text((5, 90), "  Monopoly", TFT.WHITE, sysfont, 1)

def rotary_control() -> None:
    position = 0
    menu = 0
    
    tft.fillrect((15, 60 + position), (70,2), tft.WHITE)
    tft.text((5, 50 + position), ">", TFT.WHITE, sysfont, 1)
    
    # Setup the Rotary Encoder
    button_pin = Pin(14, Pin.IN, Pin.PULL_UP)
    direction_pin = Pin(15, Pin.IN, Pin.PULL_UP)
    step_pin  = Pin(16, Pin.IN, Pin.PULL_UP)

    # for tracking the direction and button state
    previous_value = True
    button_down = False
    while True:
        if previous_value != step_pin.value():
            if step_pin.value() == False:
                # Turned Left 
                if direction_pin.value() == False:
                    if menu == 0:                   
                        tft.fillrect((15, 60 + position), (70,2), tft.BLACK)
                        tft.text((5, 50 + position), " ", TFT.WHITE, sysfont, 1)
                        position = 40
                        tft.fillrect((15, 60 + position), (70,2), tft.WHITE)
                        tft.text((5, 50 + position), ">", TFT.WHITE, sysfont, 1)
                        menu = 2;
                    else:
                        tft.fillrect((15, 60 + position), (70,2), tft.BLACK)
                        tft.text((5, 50 + position), " ", TFT.WHITE, sysfont, 1)
                        position = position - 20
                        tft.fillrect((15, 60 + position), (70,2), tft.WHITE)
                        tft.text((5, 50 + position), ">", TFT.WHITE, sysfont, 1)
                        menu = menu - 1
                # Turned Right
                else:
                    if menu == 2:                   
                        tft.fillrect((15, 60 + position), (70,2), tft.BLACK)
                        tft.text((5, 50 + position), " ", TFT.WHITE, sysfont, 1)
                        position = 0
                        tft.fillrect((15, 60 + position), (70,2), tft.WHITE)
                        tft.text((5, 50 + position), ">", TFT.WHITE, sysfont, 1)
                        menu = 0;
                    else:
                        tft.fillrect((15, 60 + position), (70,2), tft.BLACK)
                        tft.text((5, 50 + position), " ", TFT.WHITE, sysfont, 1)
                        position = position + 20
                        tft.fillrect((15, 60 + position), (70,2), tft.WHITE)
                        tft.text((5, 50 + position), ">", TFT.WHITE, sysfont, 1)
                        menu = menu + 1
            previous_value = step_pin.value()        
        # Check for button pressed
        if button_pin.value() == False and not button_down:
            button_down = True
            tft.text((5, 110), "Launching Game!", TFT.WHITE, sysfont, 1)
            utime.sleep(0.5)
            tft.fillrect((0, 110), (100,50), tft.BLACK)
            uart.write(str(menu)) # send count data to PI
        # Decbounce button
        if button_pin.value() == True and button_down:
            button_down = False
        # Wait for acknowledgement, if so break out of the menu loop
        if uart.read() == b'a':
            tft.fill(tft.BLACK)
            break
        tft.text((5, 130), "Menu Value: " + str(menu), TFT.WHITE, sysfont, 1)
        
def read_sensors() -> None:
    while True:
        # Separate for loop for Mux 0 
        for count0 in range(len(HFX_POSITIONS0)):
             # SET MUX_PINS BASED OFF COUNT
            Pin(MUX_PINS[0]).value(count0 & 0x01)
            Pin(MUX_PINS[1]).value(count0 & 0x02)
            Pin(MUX_PINS[2]).value(count0 & 0x04)
            Pin(MUX_PINS[3]).value(count0 & 0x08)
            reading0 = Sig0.read_u16()

            # get the adc reading
            print("MUX 0 ADC ", count0, " : ", reading0)
                
            if reading0 < 45000: # if reading is lower than adc value
                if(HFX_POSITIONS0[count0] > 9):
                    uart.write('t') # send count data to PI

                uart.write(b'%d'%HFX_POSITIONS0[count0]) # send count data to PI          
                print("SENT DATA FOR HFX PIN: ", HFX_POSITIONS0[count0])

            time.sleep(1) # sleep for a short time (0.1s)
            
        # Separate for loop for Mux 1   
        for count1 in range(len(HFX_POSITIONS1)):
             # SET MUX_PINS BASED OFF COUNT
            Pin(MUX_PINS[4]).value(count1 & 0x01)
            Pin(MUX_PINS[5]).value(count1 & 0x02)
            Pin(MUX_PINS[6]).value(count1 & 0x04)
            Pin(MUX_PINS[7]).value(count1 & 0x08)
            reading1 = Sig1.read_u16()

            # get the adc reading
            print("MUX 1 ADC ", count1, " : ", reading1)
                
            if reading1 < 45000: # if reading is lower than adc value
                if(HFX_POSITIONS1[count1] > 9):
                    uart.write('t') # send count data to PI

                uart.write(b'%d'%HFX_POSITIONS1[count1]) # send count data to PI           
                print("SENT DATA FOR HFX PIN: ", HFX_POSITIONS1[count1])

            time.sleep(1) # sleep for a short time (0.1s)

if __name__ == "__main__":
    test_main()
    rotary_control()
    read_sensors()