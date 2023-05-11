import serial
import board
import neopixel
import time
import random
import subprocess
import threading
import keyboard

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735
import RPi.GPIO as GPIO

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GPIO.cleanup()
print('cleaned up')

GPIO.setmode(GPIO.BCM)

ROTARY_PUSH = 13
ROTARY_ROTATE = 19
ROTARY_DIRECTION = 26


disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=128, height=160, rotation=180, invert=False)
# init uart

uart = serial.Serial("/dev/ttyS0", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 1)

# init LEDs
LEDstrip = neopixel.NeoPixel(board.D21, 121, brightness = 1)

img = Image.new('RGB', (disp.width, disp.height))
draw = ImageDraw.Draw(img)

# Load default font.
font = ImageFont.load_default()

GAMES = ["Stacker", "Tic Tac Toe", "Connect4+", "DrawIt!"]

# Menu Data
menu_position = 0
menu_selection = 0
menu_size = 0
menu_mode = 0

def draw_box(x1, y1, x2, y2):
    draw.rectangle((x1, y1, x2, y1), fill = WHITE)
    draw.rectangle((x1, y2, x2, y2), fill = WHITE)
    draw.rectangle((x1, y1, x1, y2), fill = WHITE)
    draw.rectangle((x2, y1, x2, y2), fill = WHITE)

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
    draw.text((5, 50 + menu_position), ("  " + GAMES[menu_selection]), font = font, fill = WHITE)
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
    draw.text((5, 50 + menu_position), ("  " + GAMES[menu_selection]), font = font, fill = WHITE)
    draw.text((5, 50 + menu_position), ">", font = font, fill = WHITE)
    disp.display(img)
    
# launches appropriate game based on value
def launch_game(game : int) -> None:
    if game == 0:
        print("Launching Stacker")
        subprocess.run(["python3", "StackerNoGUI.py"])
        print("closed!!!!")
    elif game == 1:
        print("Launching Connect4+")
        #subprocess.run(["python3", "Connect4DebugPi.py"])   
   
def select(pin) -> None:
    draw.rectangle((0, 135, disp.width, disp.height), fill = BLACK)
    draw.text((5, 135), ("Launching..."), font = font, fill = WHITE)
    draw.text((5, 147), (GAMES[menu_selection]), font = font, fill = WHITE)
    disp.display(img)

    print(menu_selection)
    uart.flush()
    uart.write(b'%d' % menu_selection)
      
    ack = uart.read()
    print("ack:", ack)
    
    if ack == b'a':
        print('clearing events')
        clear_events()
        
        print('starting game')
        launch_game(menu_selection)
        
        #print('adding events')
        #stop_animation()
        #launch_game(menu_selection)
        #start_animation()
        
        #add_events()
        
    else:
        print('timed out :(')
            
# function called when rotary encoder is twisted
def step(pin) -> None:
    update_menu(GPIO.input(ROTARY_DIRECTION)) # update menu based on the direction pin value (left or right)

# menu to display all the games (Tic-Tac-Toe, Connect4+, etc)
def startup_display() -> None:
    # resets menu data with menu size of the games
    reset_menu_data(len(GAMES) - 1, 0)

    clearScreen()
    draw.rectangle((0, 0, 130, 30), fill = BLUE)
    draw.rectangle((12, 48, 100, 63), fill = WHITE)
    draw.rectangle((13, 49, 99, 62), fill = ORANGE)
    draw.text((5, 7.5), "Game Select", font = font, fill = WHITE)
    for i in range(0, menu_size + 1): # displays test for every game
        draw.text((5, 50 + (20 * i)), ("  " + GAMES[i]), font = font, fill = WHITE)
    draw.text((5, 50), ">", font = font, fill = WHITE)
    disp.display(img)
    
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
    
def clear_events() -> None:
    GPIO.remove_event_detect(ROTARY_PUSH)
    GPIO.cleanup(ROTARY_PUSH)
    print("cleaned up")
    #    GPIO.remove_event_detect(ROTARY_ROTATE)
    
def add_events() -> None:
    print('in add events')
    GPIO.setup(ROTARY_PUSH, GPIO.IN, pull_up_down = GPIO.PUD_UP)    
    GPIO.add_event_detect(ROTARY_PUSH, GPIO.FALLING, callback = select, bouncetime=500)
    print('added event 1')
    #GPIO.add_event_detect(ROTARY_ROTATE, GPIO.FALLING, callback = step, bouncetime=150)
    #print('added event 2')
        
if __name__ == "__main__":
    #start_animation()
    startup_display() # start with games shown first
    
    GPIO.setup(ROTARY_PUSH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(ROTARY_PUSH, GPIO.FALLING, callback = select, bouncetime=500)
    GPIO.setup(ROTARY_ROTATE, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ROTARY_DIRECTION, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    #clear_events()
    #add_events()
    
    while True:
        pass

print("finished")
        
     