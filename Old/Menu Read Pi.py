import serial
import board
import neopixel
import time

# init uart
uart = serial.Serial("/dev/ttyS0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

# init LEDs
LEDstrip = neopixel.NeoPixel(board.D21, 121, brightness = 0.25)

# wheel function taken from neopixel sample code
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)

# rainbow_cycle function taken from neopixel sample code - modified to fit variables
def rainbow_cycle(wait):
  num_pixels = len(LEDstrip)
  
  for j in range(255):
    for i in range(num_pixels):
      pixel_index = (i * 256 // num_pixels) + j
      LEDstrip[i] = wheel(pixel_index & 255)
  LEDstrip.show()
  time.sleep(wait)

if __name__ == "__main__":
  rainbow_cycle(0.05) # start rainbow cycle
  
  while True:
    game = uart.read() # constantly wait for uart read
  
    # once uart character is found, check game variable
    if game == b'0':
        print("Launching Tic-Tac-Toe")
<<<<<<< HEAD
        with open("Connect4DebugPi.py") as f: # run shell command to launch specific game code
            exec(f.read())  
        sys.exit(0)                    # then exit this current code
    elif game == b'1':
        print("Launching Connect-4")
        with open("Connect4Pi.py") as f: # run shell command to launch specific game code
            exec(f.read())  
        sys.exit(0)                    # then exit this current code
    else:
=======
        exec(open('file.py').read()) # execute game
      case '1':
        print("Launching Connect4+")
        exec(open('file.py').read()) # execute game
      case _:
>>>>>>> 67191fbf4349e9f7fa1eecfcdd60987c0259e360
        print("No such game exists")
