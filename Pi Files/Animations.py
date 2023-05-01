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
    
    def toggle_leds(self, positions : list, color : list, delay : float) -> None:
        for i in positions:
            self.leds[i] = color
        self.leds.show()
        sleep(delay)

        for i in positions:
            self.leds[i] = self.OFF

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
        self.toggle_leds([60], self.get_random_color(), delay)
        self.toggle_leds([49, 59, 61, 71], self.get_random_color(), delay)
        self.toggle_leds([38, 48, 50, 58, 62, 70, 72, 82], self.get_random_color(), delay)
        self.toggle_leds([27, 37, 39, 47, 51, 57, 63, 69, 73, 81, 83, 93], self.get_random_color(), delay)
        self.toggle_leds([16, 26, 28, 36, 40, 46, 52, 56, 64, 68, 74, 80, 84, 92, 94, 104], self.get_random_color(), delay)
        self.toggle_leds([5, 15, 17, 25, 29, 35, 41, 45, 53, 55, 65, 67, 75, 79, 85, 91, 95, 103, 105, 115], self.get_random_color(), delay)
        self.toggle_leds([4, 6, 14, 18, 24, 30, 34, 42, 44, 54, 66, 76, 78, 86, 90, 96, 102, 106, 114, 116], self.get_random_color(), delay)
        self.toggle_leds([3, 7, 13, 19, 23, 31, 33, 43, 77, 87, 89, 97, 101, 107, 113, 117], self.get_random_color(), delay)
        self.toggle_leds([2, 8, 12, 20, 22, 32, 88, 98, 100, 108, 112, 118], self.get_random_color(), delay)
        self.toggle_leds([1, 9, 11, 21, 99, 109, 111, 119], self.get_random_color(), delay)
        self.toggle_leds([0, 10, 110, 120], self.get_random_color(), delay)
        sleep(delay)
        self.leds.auto_write = True

    def wipe_right(self, delay : float = 0.1) -> None:
        self.leds.auto_write = False
        self.toggle_leds([0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 110], self.get_random_color(), delay)
        self.toggle_leds([1, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111], self.get_random_color(), delay)
        self.toggle_leds([2, 13, 24, 35, 46, 57, 68, 79, 90, 101, 112], self.get_random_color(), delay)
        self.toggle_leds([3, 14, 25, 36, 47, 58, 69, 80, 91, 102, 113], self.get_random_color(), delay)
        self.toggle_leds([4, 15, 26, 37, 48, 59, 70, 81, 92, 103, 114], self.get_random_color(), delay)
        self.toggle_leds([5, 16, 27, 38, 49, 60, 71, 82, 93, 104, 115], self.get_random_color(), delay)
        self.toggle_leds([6, 17, 28, 39, 50, 61, 72, 83, 94, 105, 116], self.get_random_color(), delay)
        self.toggle_leds([7, 18, 29, 40, 51, 62, 73, 84, 95, 106, 117], self.get_random_color(), delay)
        self.toggle_leds([8, 19, 30, 41, 52, 63, 74, 85, 96, 107, 118], self.get_random_color(), delay)
        self.toggle_leds([9, 20, 31, 42, 53, 64, 75, 86, 97, 108, 119], self.get_random_color(), delay)
        self.toggle_leds([10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120], self.get_random_color(), delay)
        sleep(delay)
        self.leds.auto_write = True

    def wipe_left(self, delay : float = 0.1) -> None:
        self.leds.auto_write = False
        self.toggle_leds([10, 21, 32, 43, 54, 65, 76, 87, 98, 109, 120], self.get_random_color(), delay)
        self.toggle_leds([9, 20, 31, 42, 53, 64, 75, 86, 97, 108, 119], self.get_random_color(), delay)
        self.toggle_leds([8, 19, 30, 41, 52, 63, 74, 85, 96, 107, 118], self.get_random_color(), delay)
        self.toggle_leds([7, 18, 29, 40, 51, 62, 73, 84, 95, 106, 117], self.get_random_color(), delay)
        self.toggle_leds([6, 17, 28, 39, 50, 61, 72, 83, 94, 105, 116], self.get_random_color(), delay)
        self.toggle_leds([5, 16, 27, 38, 49, 60, 71, 82, 93, 104, 115], self.get_random_color(), delay)
        self.toggle_leds([4, 15, 26, 37, 48, 59, 70, 81, 92, 103, 114], self.get_random_color(), delay)
        self.toggle_leds([3, 14, 25, 36, 47, 58, 69, 80, 91, 102, 113], self.get_random_color(), delay)
        self.toggle_leds([2, 13, 24, 35, 46, 57, 68, 79, 90, 101, 112], self.get_random_color(), delay)
        self.toggle_leds([1, 12, 23, 34, 45, 56, 67, 78, 89, 100, 111], self.get_random_color(), delay)
        self.toggle_leds([0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 110], self.get_random_color(), delay)
        sleep(delay)
        self.leds.auto_write = True

    def wipe_down(self, delay : float = 0.1) -> None:
        self.leds.auto_write = False
        self.toggle_leds([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], self.get_random_color(), delay)
        self.toggle_leds([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], self.get_random_color(), delay)
        self.toggle_leds([22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], self.get_random_color(), delay)
        self.toggle_leds([33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43], self.get_random_color(), delay)
        self.toggle_leds([44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54], self.get_random_color(), delay)
        self.toggle_leds([55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65], self.get_random_color(), delay)
        self.toggle_leds([66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76], self.get_random_color(), delay)
        self.toggle_leds([77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87], self.get_random_color(), delay)
        self.toggle_leds([88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98], self.get_random_color(), delay)
        self.toggle_leds([99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109], self.get_random_color(), delay)
        self.toggle_leds([110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120], self.get_random_color(), delay)
        sleep(delay)
        self.leds.auto_write = True

    def wipe_up(self, delay : float = 0.1) -> None:
        self.leds.auto_write = False
        self.toggle_leds([110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120], self.get_random_color(), delay)
        self.toggle_leds([99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109], self.get_random_color(), delay)
        self.toggle_leds([88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98], self.get_random_color(), delay)
        self.toggle_leds([77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87], self.get_random_color(), delay)
        self.toggle_leds([66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76], self.get_random_color(), delay)
        self.toggle_leds([55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65], self.get_random_color(), delay)
        self.toggle_leds([44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54], self.get_random_color(), delay)
        self.toggle_leds([33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43], self.get_random_color(), delay)
        self.toggle_leds([22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32], self.get_random_color(), delay)
        self.toggle_leds([11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], self.get_random_color(), delay)
        self.toggle_leds([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], self.get_random_color(), delay)
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
        print("doing wipe")
        random_animation = randint(0, 5)
        if random_animation == 0:
            self.snake_animation()
        elif random_animation == 1:
            self.explosion_animation()
        elif random_animation == 2:
            self.wipe_right()
        elif random_animation == 3:
            self.wipe_left()
        elif random_animation == 4:
            self.wipe_down()
        elif random_animation == 5:
            self.wipe_up()

    def main_loop(self) -> None:
        while self.can_play:
            print("looping animation!")
            self.slide()
            self.random_wipe_animation()
            
        self.clear_board()
        self.finished = True