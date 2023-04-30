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

    def get_random_color(self) -> tuple:
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    
    # Function to make snake animation (line with defined length that moves)
    def snake_animation(self, delay : float = 0.001, length : int = 5, brightness : float = 1) -> None:
        self.leds.brightness = brightness
        
        for i in range(0, len(self.leds) + length):
            if i < len(self.leds):
                self.leds[i] = self.get_random_color()
            if length > 0 and i >= length:
                self.leds[i - length] = self.OFF
            sleep(delay)

    def explosion_animation(self, delay : float = 0.1) -> None:
        self.leds.auto_write = False
        
        positions = [60]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [49, 59, 61, 71]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [38, 48, 50, 58, 62, 70, 72, 82]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [27, 37, 39, 47, 51, 57, 63, 69, 73, 81, 83, 93]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [16, 26, 28, 36, 40, 46, 52, 56, 64, 68, 74, 80, 84, 92, 94, 104]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [5, 15, 17, 25, 29, 35, 41, 45, 53, 55, 65, 67, 75, 79, 85, 91, 95, 103, 105, 115]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [4, 6, 14, 18, 24, 30, 34, 42, 44, 54, 66, 76, 78, 86, 90, 96, 102, 106, 114, 116]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [3, 7, 13, 19, 23, 31, 33, 43, 77, 87, 89, 97, 101, 107, 113, 117]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [2, 8, 12, 20, 22, 32, 88, 98, 100, 108, 112, 118]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [1, 9, 11, 21, 99, 109, 111, 119]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        positions = [0, 10, 110, 120]
        for i in positions:
            self.leds[i] = self.get_random_color()
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF
        self.leds.show()
        sleep(delay)
        
        self.leds.auto_write = True


    def slide(self, delay : float = 1.0) -> None:
        self.leds.auto_write = False
        if self.can_play:
            self.create_B(1, (0, 125, 255))
            self.create_B(6, (255, 125, 0))
            self.create_G(67, (255, 125, 0))
            self.create_B(72, (0, 125, 255))
            self.leds.show()
            sleep(delay)
        
        if self.can_play:
            self.create_B(1, (0, 0, 0))
            self.create_B(6, (0, 0, 0))
            self.create_G(67, (0, 0, 0))
            self.create_B(72, (0, 0, 0))
            self.create_C(0, (0, 125, 255))
            self.create_S(4, (0, 125, 255))
            self.create_U(8, (0, 125, 255))
            self.create_L(67, (255, 125, 0))
            self.create_B(72, (255, 125, 0))
            self.leds.show()
            sleep(delay)

        self.leds.auto_write = True

    def random_wipe_animation(self) -> None:
        random_animation = randint(0, 1)
        if random_animation == 0:
            self.snake_animation()
        elif random_animation == 1:
            self.explosion_animation()

    def main_loop(self) -> None:
        while self.can_play:
            print("looping animation!")
            self.random_wipe_animation()
            #self.snake_animation() # delay, snake length, brightness
            self.slide()
            
        self.clear_board()
        self.finished = True