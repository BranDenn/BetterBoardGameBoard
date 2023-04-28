from GameClass import Game
from time import sleep
from random import randint

class Animations(Game):
    def create_B(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 1] = color
        self.leds[starting_position + 2] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 13] = color
        self.leds[starting_position + 22] = color
        self.leds[starting_position + 23] = color
        self.leds[starting_position + 24] = color
        self.leds[starting_position + 25] = color
        self.leds[starting_position + 33] = color
        self.leds[starting_position + 36] = color
        self.leds[starting_position + 44] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 46] = color
        self.leds[starting_position + 47] = color
        
    def create_G(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 1] = color
        self.leds[starting_position + 2] = color
        self.leds[starting_position + 3] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 22] = color
        self.leds[starting_position + 24] = color
        self.leds[starting_position + 25] = color
        self.leds[starting_position + 33] = color
        self.leds[starting_position + 36] = color
        self.leds[starting_position + 44] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 46] = color
        self.leds[starting_position + 47] = color

    def create_C(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 1] = color
        self.leds[starting_position + 2] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 22] = color
        self.leds[starting_position + 33] = color
        self.leds[starting_position + 44] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 46] = color
        
    def create_S(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 1] = color
        self.leds[starting_position + 2] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 22] = color
        self.leds[starting_position + 23] = color
        self.leds[starting_position + 24] = color
        self.leds[starting_position + 35] = color
        self.leds[starting_position + 44] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 46] = color
        
    def create_U(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 2] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 13] = color
        self.leds[starting_position + 22] = color
        self.leds[starting_position + 24] = color
        self.leds[starting_position + 33] = color
        self.leds[starting_position + 35] = color
        self.leds[starting_position + 44] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 46] = color
        
    def create_L(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 22] = color
        self.leds[starting_position + 33] = color
        self.leds[starting_position + 44] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 46] = color
        self.leds[starting_position + 47] = color
        
    def smile(self, starting_position : int, color : tuple) -> None:
        self.leds[starting_position] = color
        self.leds[starting_position + 1] = color
        self.leds[starting_position + 5] = color
        self.leds[starting_position + 6] = color
        self.leds[starting_position + 11] = color
        self.leds[starting_position + 12] = color
        self.leds[starting_position + 16] = color
        self.leds[starting_position + 17] = color
        self.leds[starting_position + 33] = color
        self.leds[starting_position + 39] = color
        self.leds[starting_position + 45] = color
        self.leds[starting_position + 49] = color
        self.leds[starting_position + 57] = color
        self.leds[starting_position + 58] = color
        self.leds[starting_position + 59] = color

    # Function to make snake animation (line with defined length that moves)
    def snake_animation(self, delay : float = 0.001, length : int = 5, brightness : float = 1) -> None:
        self.leds.brightness = brightness
        
        for i in range(0, len(self.leds) + length):
            if i < len(self.leds):
                self.leds[i] = (randint(0, 255), randint(0, 255), randint(0, 255))
            if length > 0 and i >= length:
                self.leds[i - length] = self.OFF
            sleep(delay)

    def slide(self, delay : float = 1.0) -> None:
        if self.can_play:
            self.create_B(1, (0, 125, 255))
            self.create_B(6, (255, 125, 0))
            self.create_G(67, (255, 125, 0))
            self.create_B(72, (0, 125, 255))
            sleep(delay)
            self.create_B(1, (0, 0, 0))
            self.create_B(6, (0, 0, 0))
            self.create_G(67, (0, 0, 0))
            self.create_B(72, (0, 0, 0))
        
        if self.can_play:
            self.create_C(0, (0, 125, 255))
            self.create_S(4, (0, 125, 255))
            self.create_U(8, (0, 125, 255))
            self.create_L(67, (255, 125, 0))
            self.create_B(72, (255, 125, 0))
            sleep(delay)
            self.create_C(0, (0, 0, 0))
            self.create_S(4, (0, 0, 0))
            self.create_U(8, (0, 0, 0))
            self.create_L(67, (0, 0, 0))
            self.create_B(72, (0, 0, 0))

    def main_loop(self) -> None:
        self.leds.auto_write = True
        while self.can_play:
            print("looping animation!")
            self.snake_animation() # delay, snake length, brightness
            self.slide()