import serial
import board
import neopixel
import time
import random
import subprocess
import threading
import RPi.GPIO as GPIO
import keyboard

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735

GPIO.cleanup()
print("Cleaned up GPIO!")

# init uart
uart = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

# init LEDs
LEDstrip = neopixel.NeoPixel(board.D21, 121, brightness = 1)

# can animation global variable
can_animate = True

# ---------------------------------------------- ANIMATION SECTION START ----------------------------------------------
# Function to make snake animation (line with defined length that moves)
def snake_animation(delay : float = 0.05, length : int = 0, brightness : float = 1) -> None:
    LEDstrip.brightness = brightness
    
    for i in range(0, len(LEDstrip) + length):
        if i < len(LEDstrip):
            LEDstrip[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if length > 0 and i >= length:
            LEDstrip[i - length] = (0, 0, 0)
        time.sleep(delay)
                
def create_B(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 1] = color
    LEDstrip[starting_position + 2] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 13] = color
    LEDstrip[starting_position + 22] = color
    LEDstrip[starting_position + 23] = color
    LEDstrip[starting_position + 24] = color
    LEDstrip[starting_position + 25] = color
    LEDstrip[starting_position + 33] = color
    LEDstrip[starting_position + 36] = color
    LEDstrip[starting_position + 44] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 46] = color
    LEDstrip[starting_position + 47] = color
    
def create_G(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 1] = color
    LEDstrip[starting_position + 2] = color
    LEDstrip[starting_position + 3] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 22] = color
    LEDstrip[starting_position + 24] = color
    LEDstrip[starting_position + 25] = color
    LEDstrip[starting_position + 33] = color
    LEDstrip[starting_position + 36] = color
    LEDstrip[starting_position + 44] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 46] = color
    LEDstrip[starting_position + 47] = color

def create_C(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 1] = color
    LEDstrip[starting_position + 2] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 22] = color
    LEDstrip[starting_position + 33] = color
    LEDstrip[starting_position + 44] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 46] = color
    
def create_S(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 1] = color
    LEDstrip[starting_position + 2] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 22] = color
    LEDstrip[starting_position + 23] = color
    LEDstrip[starting_position + 24] = color
    LEDstrip[starting_position + 35] = color
    LEDstrip[starting_position + 44] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 46] = color
    
def create_U(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 2] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 13] = color
    LEDstrip[starting_position + 22] = color
    LEDstrip[starting_position + 24] = color
    LEDstrip[starting_position + 33] = color
    LEDstrip[starting_position + 35] = color
    LEDstrip[starting_position + 44] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 46] = color
    
def create_L(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 22] = color
    LEDstrip[starting_position + 33] = color
    LEDstrip[starting_position + 44] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 46] = color
    LEDstrip[starting_position + 47] = color
    
def smile(starting_position : int, color : tuple) -> None:
    LEDstrip[starting_position] = color
    LEDstrip[starting_position + 1] = color
    LEDstrip[starting_position + 5] = color
    LEDstrip[starting_position + 6] = color
    LEDstrip[starting_position + 11] = color
    LEDstrip[starting_position + 12] = color
    LEDstrip[starting_position + 16] = color
    LEDstrip[starting_position + 17] = color
    LEDstrip[starting_position + 33] = color
    LEDstrip[starting_position + 39] = color
    LEDstrip[starting_position + 45] = color
    LEDstrip[starting_position + 49] = color
    LEDstrip[starting_position + 57] = color
    LEDstrip[starting_position + 58] = color
    LEDstrip[starting_position + 59] = color
    
def pulse(brightness1 : float, brightness2 : float, delay : float, amount : int) -> None:
    time.sleep(delay)
    
    random_animation = random.randint(1, 10)
    print(random_animation)
    
    if random_animation < 6:
        create_B(1, (0, 125, 255))
        create_B(6, (255, 125, 0))
        create_G(67, (255, 125, 0))
        create_B(72, (0, 125, 255))
    elif random_animation < 10:
        create_C(0, (0, 125, 255))
        create_S(4, (0, 125, 255))
        create_U(8, (0, 125, 255))
        create_L(67, (255, 125, 0))
        create_B(72, (255, 125, 0))
    else:
        smile(35, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    
    for _ in range(amount):
        LEDstrip.brightness = brightness1
        time.sleep(delay)
        LEDstrip.brightness = brightness2
        time.sleep(delay)
        
def slide(delay : float) -> None:
    if can_animate:
        create_B(1, (0, 125, 255))
        create_B(6, (255, 125, 0))
        create_G(67, (255, 125, 0))
        create_B(72, (0, 125, 255))
        time.sleep(delay)
        create_B(1, (0, 0, 0))
        create_B(6, (0, 0, 0))
        create_G(67, (0, 0, 0))
        create_B(72, (0, 0, 0))
    
    if can_animate:
        create_C(0, (0, 125, 255))
        create_S(4, (0, 125, 255))
        create_U(8, (0, 125, 255))
        create_L(67, (255, 125, 0))
        create_B(72, (255, 125, 0))
        time.sleep(delay)
        create_C(0, (0, 0, 0))
        create_S(4, (0, 0, 0))
        create_U(8, (0, 0, 0))
        create_L(67, (0, 0, 0))
        create_B(72, (0, 0, 0))
    
    if can_animate:
        smile(35, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        time.sleep(delay)
    
# thread loop to run animation 
def animation_loop() -> None:
    while can_animate:
        print("looping animation!")
        snake_animation(0.001, 5, 1.0) # delay, snake length, brightness
        #pulse(0.1, 1.0, 0.20, 5) # brightness 1, brightness 2, delay, time to pulse
        slide(1)
    
# ---------------------------------------------- ANIMATION SECTION END ----------------------------------------------

# launches appropriate game based on value
def launch_game(game : int) -> None:
    if game == 0:
        print("Launching Stacker")
        subprocess.run(["python3", "StackerNoGUI.py"])
        #subprocess.run(["python3", "StackerNoGUI.py"])
    elif game == 1:
        print("Launching Connect4+")
        subprocess.run(["python3", "Connect4DebugPi.py"])

# main super loop
# waits for uart value and corresponds that to game
def main_loop() -> None:
    while True:
        print("waiting for main menu choice...")
        #game = uart.read() # constantly wait for uart read
        game = 0
        game = int(game)
        print("uart menu read: ", game)
  
        # once uart character is found, check game variable
        stop_animation()
        #launch_game(game)
        if game == 0:
            print("Launching Stacker")
            subprocess.run(["python3", "StackerNoGUI.py"])
            print("AWDADWADAWG")
        print("TEst")
        start_animation()

        

animation_thread = threading.Thread()

# starts the animation loop with the thread
def start_animation() -> None:
    global can_animate
    global animation_thread
    
    can_animate = True
    animation_thread = threading.Thread(target = animation_loop)
    animation_thread.start()
    
    print("thread started!")
    
# stop the animation loop with the thread and clears LEDs
def stop_animation() -> None:
    global can_animate
    global animation_thread
    
    can_animate = False
    animation_thread.join()
    LEDstrip.fill((0, 0, 0))
    
    time.sleep(1)
    print("thread stopped!")

if __name__ == "__main__":
    start_animation()
    time.sleep(0.01)
    main_loop()