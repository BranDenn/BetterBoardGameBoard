import random # used to randomize first player turn
import time
import board
import neopixel
import keyboard
import sys
from threading import Thread

# VARS
ROW_COUNT = 11
COL_COUNT = 11
color = [255, 50, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
OFF = [0, 0, 0]

print(color)

# init LEDs
LEDstrip = neopixel.NeoPixel(board.D21, ROW_COUNT * COL_COUNT, brightness = 0.5, auto_write = False)

can_press = True

def loop(row : int, delay : float, length : int = 3) -> list:           
    pos = 0
    positions = [None] * length
    direction = random.randint(0, 1)

    while True:

        if direction == 0:
            for r in range(0, 11 - length):
#                 delay += random.uniform(-.5, .5)
#                 if delay < 0:
#                     delay = 0
#                 if delay > 0.5:
#                     delay = 0.5
#                 print(delay)
                for i in range(length):
                    positions[i] = row * 11 + i + r
                    LEDstrip[positions[i]] = color
                LEDstrip.show()

                if not can_press:
                    return positions
            
                time.sleep(delay)

                for i in range(length):
                    LEDstrip[positions[i]] = OFF # Need to offset this by the length of the "bar" + 1 so that the strip clears the proper LEDs
                LEDstrip.show()

                if not can_press:
                    for i in range(length):
                        LEDstrip[positions[i]] = color
                    LEDstrip.show()
                    return positions
                
                
            direction = 1

        else:
            for r in range(11 - length, 0, -1):
#                 delay += random.uniform(-.5, .5)
#                 if delay < 0:
#                     delay = 0
#                 if delay > 0.5:
#                     delay = 0.5
#                 print(delay)
                for i in range(length):
                    positions[i] = pos = row * 11 + i + r
                    LEDstrip[positions[i]] = color
                LEDstrip.show()

                if not can_press:
                    return positions

                time.sleep(delay)
                
                for i in range(length):
                    LEDstrip[positions[i]] = OFF
                LEDstrip.show()

                if not can_press:
                    for i in range(length):
                        LEDstrip[positions[i]] = color
                    LEDstrip.show()
                    return positions
                
            direction = 0
      
use = True
def stop() -> None:  
    global can_press
    while use:
        if can_press and keyboard.is_pressed('space'):
            can_press = False
            
def push_stop() -> None:
    global can_press
    can_press = False
            
thread = Thread(target = stop)
thread.start()    
    
initial_length = 3           
blink_amount = 2

def main() -> None:
    while True:
        length = initial_length
        print("game started")

        for i in range(10, -1, -1):
            color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            speed = (i + 1) / 100
            print(speed)        
            positions = loop(i, speed, length)
        
            if i < 10:                              
                drop_positions = []
                for j in positions:
                    if LEDstrip[j + 11] == OFF:
                        LEDstrip[j] = OFF
                        drop_positions.append(j)
                    LEDstrip.show()
                
                if len(drop_positions) > 0:
                    for b in range(blink_amount):
                        time.sleep(0.5 / blink_amount)

                        for j in drop_positions:
                            LEDstrip[j] = color
                        LEDstrip.show()

                        time.sleep(0.5 / blink_amount)

                        for j in drop_positions:
                            LEDstrip[j] = OFF
                        LEDstrip.show()  
            
                    length -= len(drop_positions)
                
    #             if i < 6 and length == 3:
    #                 length -= 1
    #                 
    #             if i < 3 and length == 2:
    #                 length -= 1
            
            time.sleep(0.1)                     
            can_press = True

            if length == 0:
                print("you lost :(")
                time.sleep(1.0)
                break

            elif i == 0:
                print("you won! :)")
                for j in range(0, 121):
                    if LEDstrip[j] == color:     
                        LEDstrip[j] = [255, 255, 255]           
                    LEDstrip.show()
               
                time.sleep(2.0)
                break
           
        LEDstrip.fill(OFF)
        LEDstrip.show()
        
        #inp = int(input("play again:? 0 = NO, 1 = YES : "))
        #print(inp)
        #if inp == 0:
        print("brekaing")
        break
    
main()
use = False
thread.join()
print("out")

  

