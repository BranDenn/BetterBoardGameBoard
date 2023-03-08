# import tkinter # GUI library
# import customtkinter # Modern tkinter GUI library extention
import random # used to randomize first player turn
import board
import neopixel
import serial
from time import sleep

# The purpose of this program is to test the LED's functionality when recieving a signal from the HFX sensor.
# This will light up the corresponding LED on top of the HFX activated. 

# init uart
uart = serial.Serial("/dev/ttyS0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

# init LED strip
LEDstrip = neopixel.NeoPixel(board.D18, 9, brightness = 1)

# ARRAY VARS
player = '' # declare player as character
board = [] # declare board as array

def update_LED(position) -> None: #updates the LED strip based on the hall effect sensor input from the UART
    LEDstrip[position] = (0,0,225)
def start() -> None: # initializes the board
  global board # get the global board variable to update
  global player # get the global player variable to update

  board = [''] * 9 # clears board 
  # ['', '', '', 
  #  '', '', '',
  #  '', '', '']
  LEDstrip.fill((0, 0, 0))
  
if __name__ == "__main__":
    start() # start the game
    
    while True:
        position = int(uart.read()) # constantly wait for uart read
        update_LED(position) # once data is found, check the board position