from GameClass import Game
from time import sleep
from random import randint

class Stacker(Game):
    def __init__(self) -> None:
        super().__init__()
        self.STARTING_LENGTH = 3
        self.BLINK_AMOUNT = 2
        self.BLINK_SPEED = 0.20
        self.SPEED_DIVISOR = 100
        self.stop_movement = False

    def move(self, row : int, length : int, color : list, delay : float) -> list:
        positions = [None] * length
        direction = randint(0, 1)

        while True:
            if direction:
                for column in range(0, self.COLUMNS - length):

                    # turn on LEDs
                    for pos in range(length):
                        positions[pos] = row * self.ROWS + pos + column
                        self.leds[positions[pos]] = color
                    self.leds.show()

                    if self.stop_movement or not self.can_play:
                        return positions
                
                    sleep(delay)

                    # turn off LEDs
                    for pos in range(length):
                        self.leds[positions[pos]] = self.OFF
                    self.leds.show()

                    # in case movement was stopped when lights were turned off
                    # turn back on lights for better display
                    if self.stop_movement or not self.can_play:
                        for pos in range(length):
                            self.leds[positions[pos]] = color
                        self.leds.show()
                        return positions
                
                direction = 0

            else:
                for column in range(11 - length, 0, -1):
                    
                    # turn on LEDs
                    for pos in range(length):
                        positions[pos] = row * 11 + pos + column
                        self.leds[positions[pos]] = color
                    self.leds.show()

                if self.stop_movement or not self.can_play:
                        return positions
                
                sleep(delay)

                # turn off LEDs
                for pos in range(length):
                    self.leds[positions[pos]] = self.OFF
                self.leds.show()

                # in case movement was stopped when lights were turned off
                # turn back on lights for better display
                if self.stop_movement or not self.can_play:
                    for pos in range(length):
                        self.leds[positions[pos]] = color
                    self.leds.show()
                    return positions
                
            direction = 1

    def blink(self, positions_to_remove : list, color : list) -> None:
        for _ in self.BLINK_AMOUNT:
            sleep(self.BLINK_AMOUNT)
            for pos in positions_to_remove:
                self.leds[pos] = color
            self.leds.show()

            sleep(self.BLINK_AMOUNT)
            for pos in positions_to_remove:
                self.leds[pos] = self.OFF
            self.leds.show()
    
    def highlight_positions(self, color : list, desired_color : list) -> None:
        for pos in range(self.COLUMNS * self.ROWS):
            if self.leds[pos] == color:
                self.leds[pos] = desired_color
            self.leds.show()

    def main_loop(self) -> None:
        while self.can_play:
            print("game started")
            current_length = self.STARTING_LENGTH

            for row in range(self.ROWS - 1, -1, -1):
                color = [randint(0, 255), randint(0, 255), randint(0, 255)]
                speed = (row + 1) / self.SPEED_DIVISOR
                positions =  self.move(row, current_length, color, speed)

                if row < self.ROWS - 1:
                    positions_to_remove = []

                    for pos in positions:
                        # check if row under is free
                        if self.leds[pos + 11] == self.OFF:
                            positions_to_remove.append(pos)
                            self.leds[pos] = self.OFF
                        self.leds.show()

                    if positions_to_remove:
                        self.blink(positions_to_remove, color)
                        current_length -= len(positions_to_remove)

                sleep(0.1)
                self.stop_movement = False
                
                if current_length < 1:
                    print("you lost")
                    self.highlight_positions(color, [255, 0, 0])
                    sleep(1)
                
                elif row < 1:
                    print("you won")
                    self.highlight_positions(color, [255, 255, 255])
                    sleep(2)
                    break
                
            self.leds.fill(self.OFF)
            self.leds.show()

