import time
start_time = time.time()

import serial
import board
import neopixel
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import ST7735
import RPi.GPIO as GPIO
from pygame import mixer
#from pygame import 

# GAME IMPORTS
from Animations import Animations
from Stacker import Stacker
from Connect4 import Connect4
from TicTacToe import TicTacToe
from Draw import Draw

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

disp = ST7735.ST7735(port=0, cs=1, dc=24, backlight=23, rst=25, width=128, height=160, rotation=0, invert = False)
# init uart

uart = serial.Serial("/dev/ttyS0", baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout = 1)

# init LEDs
LEDstrip = neopixel.NeoPixel(board.D21, 121, brightness = 1)

img = Image.new('RGB', (disp.width, disp.height))
draw = ImageDraw.Draw(img)

# Load default font.
#font = ImageFont.load_default()
#font = ImageFont.truetype("IBMPlexSans-SemiBold.ttf", 14)
font = ImageFont.truetype("/home/b1128c/BetterBoardGameBoard/Pi Files/fonts/PressStart2P-Regular.ttf", 8)
font2 = ImageFont.truetype("/home/b1128c/BetterBoardGameBoard/Pi Files/fonts/PressStart2P-Regular.ttf", 36)

#Inits for pygame audio
mixer.init()
select_sound = mixer.Sound("/home/b1128c/BetterBoardGameBoard/Pi Files/audio/gameselect.wav")
music = mixer.music.load("/home/b1128c/BetterBoardGameBoard/Pi Files/audio/gamebg.wav")

# Need to declare the sound object that is being modified and then the value of the desired volume for the sound
#mixer.Sound.set_volume(select_sou, 0.1)

GAMES = ["Stacker", "Connect4+", "Tic-Tac-Toe", "Draw"]
saves = []

# create default game as the animation
game = Animations(LEDstrip)

# Menu Data
menu_position = 0
menu_selection = 0
menu_size = 0
menu_mode = 0

game_selection = 0

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
    print("MENU SELECTION:", menu_selection)
    
# scrolls the menu either up or down and updates the global selection
def update_menu(value : bool) -> None:
    global menu_position
    global menu_selection
    
    draw.rectangle((0, 46 + menu_position, disp.width - 12, 60 + menu_position), fill = BLACK)
    if menu_mode == 0:
        draw.text((disp.width * (1/2) - (font.getlength(GAMES[menu_selection]) / 2), 50 + menu_position), GAMES[menu_selection], font = font, fill = WHITE)
    else:
        draw.text((disp.width * (1/2) - (font.getlength(saves[menu_selection]) / 2), 50 + menu_position), saves[menu_selection], font = font, fill = WHITE)
   
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
    
    draw.rectangle((12, 46 + menu_position, disp.width - 12, 60 + menu_position), fill = WHITE)
    draw.rectangle((13, 47 + menu_position, disp.width - 13, 59 + menu_position), fill = RED)
    
    if menu_mode == 0:
        draw.text((disp.width * (1/2) - (font.getlength(GAMES[menu_selection]) / 2), 50 + menu_position), GAMES[menu_selection], font = font, fill = WHITE)
    else:
        draw.text((disp.width * (1/2) - (font.getlength(saves[menu_selection]) / 2), 50 + menu_position), saves[menu_selection], font = font, fill = WHITE)
    #draw.text((5, 50 + menu_position), ">", font = font, fill = WHITE)
    disp.display(img)
    
# function called when rotary encoder is twisted
def step(pin) -> None:
    global can_use
    if can_use and menu_mode != 1:
        can_use = False
        update_menu(GPIO.input(ROTARY_DIRECTION)) # update menu based on the direction pin value (left or right)
        can_use = True

# launches appropriate game based on value
def launch_game(selection : int, save_selection : int = 0) -> None:
    global game
    global menu_mode

    mixer.music.play()
    if selection == 0:
        print("Launching Stacker")
        game = Stacker(LEDstrip, disp, img, draw, font, font2)
    elif selection == 1:
        print("Launching Connect4+")
        if menu_selection == 0:
            string = saves[len(saves)-1]
            last_file_number = int(string[5:len(string)])
        else:
            last_file_number = 0
        
        if len(saves) > 1:
            game = Connect4(LEDstrip, disp, img, draw, font, font2, uart, menu_selection, last_file_number)
        else:
            game = Connect4(LEDstrip, disp, img, draw, font, font2, uart, 0, last_file_number)
            
    elif selection == 2:
        game = TicTacToe(LEDstrip, disp, img, draw, font, font2, uart)
    elif selection == 3:
        game = Draw(LEDstrip, disp, img, draw, font, font2, uart)
    else:
        game = Animations(LEDstrip)

    menu_mode = 1

def remove_game() -> None:
    global game
    game.can_play = False
    while not game.finished:
        time.sleep(0.1)
    del game
    mixer.music.stop()
    
def select(pin) -> None:
    global can_use
    global game
    global menu_mode
    if menu_mode == 0:
        if not GPIO.input(ROTARY_PUSH) and can_use:
            can_use = False
            
            mixer.Sound.play(select_sound)
            
            draw.text((5, 135), ("Trying to start"), font = font, fill = WHITE)
            draw.text((5, 145), GAMES[menu_selection] + "...", font = font, fill = WHITE)
            disp.display(img)

            if has_saves(menu_selection):
                time.sleep(1)
                can_use = True
                return

            uart.write(b'Pi%d\n' % menu_selection)
            ack = uart.readline()
            print("ack:", ack)
            
            if ack:
                remove_game()
                launch_game(menu_selection)
                time.sleep(0.5)
                can_use = True
                return
                
            else:
                print('timed out :(')
                 
    elif menu_mode == 1:
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
                remove_game()
                launch_game(-1)
                #time.sleep(1)
                #startup_display()
                startup_display()
                time.sleep(1)
                #startup_display()
                can_use = True
                return
            
    if menu_mode == 2:
        if not GPIO.input(ROTARY_PUSH) and can_use:
            can_use = False
            
            mixer.Sound.play(select_sound)
            
            draw.text((5, 135), "Trying to", font = font, fill = WHITE)
            draw.text((5, 145), "load save...", font = font, fill = WHITE)
            disp.display(img)

            uart.write(b'Pi%d\n' % game_selection)
            ack = uart.readline()
            print("ack:", ack)
            
            if ack:
                remove_game()
                launch_game(game_selection, menu_selection)
                menu_mode = 1
                time.sleep(0.5)
                can_use = True
                return
                
            else:
                print('timed out :(')
    
    can_use = True
            
# menu to display all the games (Tic-Tac-Toe, Connect4+, etc)
def startup_display() -> None:
    # resets menu data with menu size of the games
    reset_menu_data(len(GAMES) - 1, 0)

    draw.rectangle((0, 0, disp.width, disp.height), fill = BLACK)
    draw.rectangle((0, 0, disp.width, 30), fill = RED)
    draw.rectangle((0, disp.height - 30, disp.width, disp.height), fill = RED)
    text = "Game Select"
    draw.text((disp.width * (1/2) - (font.getlength(text) / 2), 12), text, font = font, fill = WHITE)

    draw.rectangle((12, 46, disp.width - 12, 60), fill = WHITE)
    draw.rectangle((13, 47, disp.width - 13, 59), fill = RED)
    for i in range(0, menu_size + 1): # displays test for every game
        draw.text((disp.width * (1/2) - (font.getlength(GAMES[i]) / 2), 50 + (20 * i)), GAMES[i], font = font, fill = WHITE)
    disp.display(img)
    
def has_saves(selection : int) -> bool:
    if selection == 1:
        global saves
        
        saves = ["NEW GAME"]
        json_files = [pos_json for pos_json in os.listdir("/home/b1128c/BetterBoardGameBoard/Pi Files/saves") if pos_json.endswith('.json')]# and pos_json.startswith("connect")]
        json_files.sort()
        
        print(json_files)
        for i in range(0, len(json_files)):
            saves.append("SAVE %d" % (int(json_files[i][5:json_files[i].rfind(".")])) )
        
        if json_files:
            global game_selection
            game_selection = selection
            save_display()
            return True

    return False

def save_display() -> None:
    if len(saves) > 3: # only allow up to 5 saves shown
        reset_menu_data(3, 2)
    else:
        reset_menu_data(len(saves) - 1, 2)
        
    print(saves)

    draw.rectangle((0, 0, disp.width, disp.height), fill = BLACK)
    draw.rectangle((0, 0, disp.width, 30), fill = RED)
    draw.rectangle((0, disp.height - 30, disp.width, disp.height), fill = RED)
    text = "Save Select"
    draw.text((disp.width * (1/2) - (font.getlength(text) / 2), 12), text, font = font, fill = WHITE)

    draw.rectangle((12, 46, disp.width - 12, 60), fill = WHITE)
    draw.rectangle((13, 47, disp.width - 13, 59), fill = RED)
    for i in range(0, menu_size + 1): # displays test for every save
        draw.text((disp.width * (1/2) - (font.getlength(saves[i]) / 2), 50 + (20 * i)),saves[i], font = font, fill = WHITE)
    disp.display(img)

if __name__ == "__main__":
    startup_display()
    
    GPIO.setup(ROTARY_PUSH, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ROTARY_ROTATE, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(ROTARY_DIRECTION, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(ROTARY_PUSH, GPIO.FALLING, callback = select, bouncetime = 500)
    GPIO.add_event_detect(ROTARY_ROTATE, GPIO.FALLING, callback = step, bouncetime = 500)

    print("SETUP COMPLETED IN %ss" % "{:.4f}".format(time.time() - start_time))
    del start_time
    
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
            #print("could not run main_loop, trying again in 0.1s...")
            time.sleep(0.1)
            
mixer.music.stop()
LEDstrip.fill([0, 0, 0])
LEDstrip.show()
GPIO.remove_event_detect(ROTARY_PUSH)
GPIO.remove_event_detect(ROTARY_ROTATE)
GPIO.cleanup()
print("cleaned up!")