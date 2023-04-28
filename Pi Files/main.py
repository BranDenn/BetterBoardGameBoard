import serial
import board
import neopixel
import time
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735
import RPi.GPIO as GPIO

# GAME IMPORTS
from Animations import Animations
from Stacker import Stacker

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GPIO.setmode(GPIO.BCM)

ROTARY_PUSH = 13
ROTARY_ROTATE = 19
ROTARY_DIRECTION = 26
can_use = True

disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=128, height=160, rotation=180, invert=False)
# init uart

uart = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 1)

# init LEDs
LEDstrip = neopixel.NeoPixel(board.D21, 121, brightness = 1)

img = Image.new('RGB', (disp.width, disp.height))
draw = ImageDraw.Draw(img)

# Load default font.
font = ImageFont.load_default()

GAMES = ["Stacker", "Tic-Tac-Toe", "Connect4+", "DrawIt!"]

# create default game as the animation
game = Animations(LEDstrip)

# Menu Data
menu_position = 0
menu_selection = 0
menu_size = 0
menu_mode = 0

# resets the data for the menu with data depeneded on the menu mode
def reset_menu_data(size : int, mode : int) -> None:
    global menu_position
    global menu_selection
    global menu_size
    global menu_mode

    menu_position = 0
    menu_selection = 0
    menu_size = size
    menu_mode = mode
    
def clearScreen() -> None:
    draw.rectangle((0, 0, disp.width, disp.height), fill = BLACK) # fill colors are (Blue, Green, Red)

# scrolls the menu either up or down and updates the global selection
def update_menu(value : bool) -> None:
    global menu_position
    global menu_selection

    draw.rectangle((0, 48 + menu_position, 100, 63 + menu_position), fill = BLACK)
    draw.text((10, 50 + menu_position), (GAMES[menu_selection]), font = font, fill = WHITE)
    if not value:
        # Turned Right
        if menu_selection == menu_size:                   
            menu_position = 0
            menu_selection = 0 
        else:
            menu_position = menu_position + 20
            menu_selection += 1
    else:
        # Turned Left
        if menu_selection == 0:                   
            menu_position = 20 * menu_size
            menu_selection = menu_size
        else:
            menu_position = menu_position - 20
            menu_selection -= 1
            
    draw.rectangle((12, 48 + menu_position, 100, 63 + menu_position), fill = WHITE)
    draw.rectangle((13, 49 + menu_position, 99, 62 + menu_position), fill = ORANGE)
    draw.text((10, 50 + menu_position), GAMES[menu_selection], font = font, fill = WHITE)
    draw.text((5, 50 + menu_position), ">", font = font, fill = WHITE)
    disp.display(img)
    
# function called when rotary encoder is twisted
def step(pin) -> None:
    global can_use
    if can_use:
        can_use = False
        update_menu(GPIO.input(ROTARY_DIRECTION)) # update menu based on the direction pin value (left or right)
        can_use = True

# launches appropriate game based on value
def launch_game(selection : int) -> None:
    global game
    if selection == 0:
        print("Launching Stacker")
        game = Stacker(LEDstrip)
    elif selection == 1:
        print("Launching Connect4+")
        #subprocess.run(["python3", "Connect4DebugPi.py"])
    else:
        game = Animations(LEDstrip)
        
   
def select(pin) -> None:
    global can_use
    global game
    global menu_mode
    print('menu_mode:', menu_mode)
    print(game)
    
#     if GPIO.input(ROTARY_PUSH) == previous_input:
#         return
    
    if menu_mode == 0:
        if not GPIO.input(ROTARY_PUSH) and can_use:
            can_use = False
            
            draw.rectangle((0, 135, disp.width, disp.height), fill = BLACK)
            draw.text((5, 135), ("Attempting to launch"), font = font, fill = WHITE)
            draw.text((5, 145), GAMES[menu_selection] + "...", font = font, fill = WHITE)
            disp.display(img)

            uart.write(b'%d' % menu_selection)
            ack = uart.read()
            print("ack:", ack)
            ack = b'0'
            
            if ack == b'0':
                game.can_play = False
                del game
                #time.sleep(1)
                launch_game(menu_selection)
                menu_mode = 1
                time.sleep(1)
                can_use = True
                return
                
            else:
                 print('timed out :(')
                 
    elif menu_mode == 1:
        print(menu_mode)
        
        start_time = time.time()
        hold_time = 0
        if not GPIO.input(ROTARY_PUSH) and can_use:
            can_use = False
            
            while not GPIO.input(ROTARY_PUSH):
                hold_time = time.time() - start_time
                if hold_time >= 2:
                    break
            
            if hold_time < 2:
                if menu_selection == 0:
                    game.stop_movement = True
            else:
                print("BROKEN")
                game.can_play = False
                del game
                launch_game(-1)
                startup_display()
                time.sleep(1)
                can_use = True
                return
    
    can_use = True
            
# menu to display all the games (Tic-Tac-Toe, Connect4+, etc)
def startup_display() -> None:
    # resets menu data with menu size of the games
    reset_menu_data(len(GAMES) - 1, 0)

    clearScreen()
    draw.rectangle((0, 0, 130, 30), fill = BLUE)
    draw.text((5, 7.5), "Game Select", font = font, fill = WHITE)

    draw.rectangle((12, 48, 100, 63), fill = WHITE)
    draw.rectangle((13, 49, 99, 62), fill = ORANGE)
    for i in range(0, menu_size + 1): # displays test for every game
        draw.text((10, 50 + (20 * i)), GAMES[i], font = font, fill = WHITE)
    draw.text((5, 50), ">", font = font, fill = WHITE)
    disp.display(img)
    
if __name__ == "__main__":
    startup_display()
    

    print(dir(GPIO))
    GPIO.setup(ROTARY_PUSH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ROTARY_ROTATE, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ROTARY_DIRECTION, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(ROTARY_PUSH, GPIO.FALLING, callback = select, bouncetime = 100)
    GPIO.add_event_detect(ROTARY_ROTATE, GPIO.FALLING, callback = step, bouncetime = 100)
    
    while True:

        try:
            print(game)
            game.main_loop()
            print("game ended")
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("keyboard interrupt")
            break
        except:
            print("could not run main_loop, trying again in 0.1s...")
            time.sleep(0.1)
            
GPIO.remove_event_detect(ROTARY_PUSH)
GPIO.remove_event_detect(ROTARY_ROTATE)
GPIO.cleanup()
print("cleaned up!")