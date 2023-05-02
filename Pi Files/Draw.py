from GameClass import Game
from random import randint

class Draw(Game):
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, font2 = None, uart = None) -> None:
        super().__init__(leds, display, image, draw, font, font2)
        self.uart = uart
        self.game_display()

    def update_board(self, position : int) -> None:
        self.leds[position] = (randint(0, 255), randint(0, 255), randint(0, 255))

    def main_loop(self) -> None:
        while self.can_play:
            position = self.uart.readline()

            if position:
                self.update_board(int(position))
                
        self.finished = True

