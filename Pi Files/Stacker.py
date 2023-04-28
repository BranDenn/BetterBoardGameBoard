from GameClass import Game
from time import sleep
from random import randint

class Stacker(Game):
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None) -> None:
        super().__init__(leds, display, image, draw, font)
        self.STARTING_LENGTH = 3
        self.BLINK_AMOUNT = 2
        self.BLINK_SPEED = 0.20
        self.SPEED_DIVISOR = 50
        self.stop_movement = False
        self.leds.auto_write = False
        self.points = 0

    def move(self, row : int, length : int, color : list, delay : float) -> list:
        positions = [None] * length
        direction = randint(0, 1)

        while self.can_play:
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
                for column in range(self.COLUMNS - length, 0, -1):
                    
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
        for _ in range(self.BLINK_AMOUNT):
            sleep(self.BLINK_SPEED)
            for pos in positions_to_remove:
                self.leds[pos] = color
            self.leds.show()

            sleep(self.BLINK_SPEED)
            for pos in positions_to_remove:
                self.leds[pos] = self.OFF
            self.leds.show()
    
    def highlight_positions(self, desired_color : list) -> None:
        for pos in range(0, self.COLUMNS * self.ROWS):
            if self.leds[pos] != self.OFF:
                self.leds[pos] = desired_color
            self.leds.show()

    def check_for_removal(self, row : int, positions : list, color : list) -> int:
        positions_to_remove = []
        if row < self.ROWS - 1:

            for pos in positions:
                # check if row under is free
                if self.leds[pos + self.ROWS] == self.OFF:
                    positions_to_remove.append(pos)
                    self.leds[pos] = self.OFF
                self.leds.show()

            if positions_to_remove:
                self.blink(positions_to_remove, color)
        
        return len(positions_to_remove)

    def game_ended(self, row : int, length : int) -> bool:
        if length < 1:
            print("you lost :(")
            self.highlight_positions(self.RED)
            sleep(1)
            return True

        if row < 1:
            print("you won :D")
            self.highlight_positions(self.WHITE)
            sleep(2)
            return True

        return False

    def update_score(self, points_amount : int) -> None:
        self.points += points_amount
        self.update_display({"Points" : self.points})

    def main_loop(self) -> None:
        self.update_display({"Points" : self.points})
        while self.can_play:
            print("game started")
            current_length = self.STARTING_LENGTH

            for row in range(self.ROWS - 1, -1, -1):
                print('row:', row)
                color = [randint(0, 255), randint(0, 255), randint(0, 255)]
                speed = (row + 1) / self.SPEED_DIVISOR
                positions = self.move(row, current_length, color, speed)
                current_length -= self.check_for_removal(row, positions, color)

                sleep(0.1)
                self.stop_movement = False
                self.update_score(current_length)

                
                if self.game_ended(row, current_length):
                    break
            
            self.leds.fill(self.OFF)
            self.leds.show()

