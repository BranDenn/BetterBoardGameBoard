from GameClass import Game
from time import sleep
from random import randint

class TicTacToe(Game):
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, font2 = None, uart = None) -> None:
        super().__init__(leds, display, image, draw, font, font2)
        self.uart = uart
        self.current_player = None
        self.red_points = 0
        self.blue_points = 0
        self.GAME_ROWS = 3
        self.GAME_COLUMNS = 3
        self.start_game()

    def set_starting_player(self) -> None:
        random_player = randint(0, 1)
        if random_player:
            self.current_player = self.RED
            self.create_border((100, 0, 0))
        else:
            self.current_player = self.BLUE
            self.create_border((0, 0, 100))
        
    def update_board(self, position : int) -> None:
        if self.leds[position] == self.DIM_WHITE:
            self.leds[position] = self.current_player
            self.check_win(position)
        else:
            print("position:", position, "is already taken")

    def create_border(self, color : list) -> None:
        positions = [24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41, 46, 47, 51, 52, 57, 58, 62, 63, 68, 69, 73, 74, 79, 80, 81, 82, 83, 84, 85, 90, 91, 92, 93, 94, 95, 96]
        for pos in positions:
            self.leds[pos] = color

    def create_inner(self, color : list) -> None:
        positions = [48, 49, 50, 59, 60, 61, 70, 71, 72]
        for pos in positions:
            self.leds[pos] = color

    def next_player(self) -> None:
        self.leds.auto_write = False
        if self.current_player == self.RED:
            self.current_player = self.BLUE
            self.create_border((0, 0, 50))
        else:
            self.current_player = self.RED
            self.create_border((50, 0, 0))

        self.leds.show()
        self.leds.auto_write = True

    def show_win(self, winning_positions : list) -> None:
        self.play_win_sound()
        for i in winning_positions:
            self.leds[i] = [0, 255, 0]
            sleep(0.1)

    def is_row_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 3):
            scan_position = position + i
            
            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break
            
        for i in range(1, 3):
            scan_position = position - i

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break
        
        if len(winning_positions) >= 3:
            self.show_win(winning_positions)
            return True
        return False
    
    def is_col_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 3):
            scan_position = position + (i * self.COLUMNS)

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 3):
            scan_position = position - (i * self.COLUMNS)

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 3:
            self.show_win(winning_positions)
            return True
        return False

    def is_diag_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 3):
            scan_position = position + (i * self.COLUMNS) + i

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 3):
            scan_position = position - (i * self.COLUMNS) - i #96, 84, 81, 67

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 3:
            self.show_win(winning_positions)
            return True
    
        winning_positions = [position]

        for i in range(1, 3):
            scan_position = position + (i * self.COLUMNS) - i

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 3):
            scan_position = position - (i * self.COLUMNS) + i

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
        return False
    
    def check_win(self, position : int) -> None:

        if self.is_row_win(position) or self.is_col_win(position) or self.is_diag_win(position):
            self.update_score(1)
            sleep(2.5)
            self.start_game()

        elif self.DIM_WHITE not in self.leds:
            self.create_border([255, 127, 0])
            sleep(2.5)
            self.start_game()

        else:
            self.next_player()
        
    def update_score(self, points : int = 0):
        if self.current_player == self.RED:
            self.red_points += points
        else:
            self.blue_points += points

        self.draw.rectangle((0, 50, self.disp.width, self.disp.height - 50), fill = (255, 255, 255))
        bounds1 = self.font2.getbbox(str(self.red_points))[2:4]
        bounds2 = self.font2.getbbox(str(self.blue_points))[2:4]
        bounds1 = (self.disp.width * (1/4) - bounds1[0] * (1/2), self.disp.height * (1/2) - bounds1[1] * (1/2))
        bounds2 = (self.disp.width * (3/4) - bounds2[0] * (1/2), self.disp.height * (1/2) - bounds2[1] * (1/2))
        self.draw.text(bounds1, str(self.red_points), font = self.font2, fill = (0, 0, 255))
        self.draw.text(bounds2, str(self.blue_points), font = self.font2, fill = (255, 0, 0))
        self.disp.display(self.img)

    def start_game(self) -> None:
        self.leds.auto_write = False
        self.create_inner(self.DIM_WHITE)
        self.game_display()
        self.update_score()
        self.set_starting_player()
        self.leds.show()
        self.leds.auto_write = True

    def main_loop(self) -> None:
        while self.can_play:
            position = self.uart.readline()

            if position:
                self.update_board(int(position))
                
        self.finished = True

