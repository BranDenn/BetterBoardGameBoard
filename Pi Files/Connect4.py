from GameClass import Game
from time import sleep
from random import randint

class Connect4(Game):
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, uart = None) -> None:
        super().__init__(leds, display, image, draw, font)
        self.uart = uart
        self.current_player
        self.leds.auto_write = True
        self.red_points = 0
        self.blue_points = 0
        self.GAME_ROWS = 7
        self.GAME_COLUMNS = 7
        self.font.size = 24
        self.start_game()

    def set_starting_player(self) -> None:
        random_player = randint(0, 1)
        if random_player:
            self.current_player = self.RED
        else:
            self.current_player = self.BLUE
        
    def update_board(self, position : int) -> None:
        position = (position % self.COLUMNS) + (self.ROWS + self.ROWS)

        if self.leds[position] == self.OFF:
            for i in range(0, self.GAME_ROWS):
                self.leds[position] = self.current_player

                if i < (self.COLUMNS - 2) and self.leds[position + self.ROWS] == self.OFF:
                    sleep(0.05)
                    self.leds[position] = self.OFF
                    position += self.ROWS

        else:
            print("position:", position, "is already taken")

    def create_border(self, color : list) -> None:
        self.leds.brightness = 0.1

        positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 31, 32, 33, 34, 42, 43, 44, 45, 53, 54, 55, 56, 64, 65, 66, 67, 75, 76, 77, 78, 86, 87, 88, 89, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]

        for pos in positions:
            self.leds[pos] = color

        self.leds.brightness = 1

    def next_player(self) -> None:
        if self.current_player == self.RED:
            self.current_player = self.BLUE
        else:
            self.current_player = self.RED

        self.create_border(self.current_player)

    def show_win(self, winning_positions : list) -> None:
        for i in winning_positions:
            self.leds[i] = self.WHITE
            sleep(0.25)

    def is_row_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            scan_position = position + i
            if scan_position % self.GAME_COLUMNS == 0:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break
        
        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
        return False
    
    def is_col_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            scan_position = position + (i * self.GAME_COLUMNS)
            if scan_position >= 42:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
            scan_position = position - (i * self.GAME_COLUMNS)
            if scan_position < 0:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
        return False

    def is_diag_win_1(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            scan_position = position + (i * self.GAME_COLUMNS) + i
            if scan_position >= 42 or scan_position % self.GAME_COLUMNS == 0:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
            scan_position = position - (i * self.GAME_COLUMNS) - i
            if scan_position < 0 or scan_position % self.GAME_COLUMNS == 6:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
        return False
    
    def is_diag_win_2(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            scan_position = position + (i * self.GAME_COLUMNS) - i
            if scan_position >= 42 or scan_position % self.GAME_COLUMNS == 6:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
            scan_position = position + (i * self.GAME_COLUMNS) - i
            if scan_position < 0 or scan_position % self.GAME_COLUMNS == 0:
                break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
        return False
    
    def check_win(self, position : int) -> None:

        if self.is_row_win(position) or self.is_col_win(position) or self.is_diag_win_1(position) or self.is_diag_win_2(position):
            self.update_score(1)
            sleep(2.5)
        
        elif self.OFF not in self.leds:
            self.create_border([255, 127, 0])
            sleep(2.5)

        else:
            self.next_player()
        
    def update_score(self, points : int = 0):
        if self.current_player == self.RED:
            self.red_points += points
        else:
            self.blue_points += points

        self.draw.rectangle((0, 50, self.disp.width, self.disp.height - 50), fill = (0, 0, 0))
        self.draw.text((self.disp.width * (1/4), self.disp.height * (1/2)), str(self.red_points), font = self.font, fill = (255, 0, 0))
        self.draw.text((self.disp.width * (3/4), self.disp.height * (1/2)), str(self.blue_points), font = self.font, fill = (0, 0, 255))
        self.disp.display(self.img)

    def start_game(self) -> None:
        self.leds.fill(self.OFF)
        self.game_display({"Red Points" : self.red_points, "Blue Points" : self.blue_points})
        self.set_starting_player()
        self.create_border(self.current_player)

    def game_loop(self) -> None:
        while self.can_play:
            position = self.uart.read()
            if position:
                self.update_board(int(position))
            else:
                print("connect 4 uart timed out, trying again...")
