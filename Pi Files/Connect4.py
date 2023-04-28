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
        self.GAME_ROWS = 6
        self.GAME_COLUMNS = 7
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

        positions = []

        for pos in positions:
            self.leds[pos] = color

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

        self.update_display({"Red Points" : self.red_points, "Blue Points" : self.blue_points})

    def start_game(self) -> None:
        self.leds.fill(self.OFF)
        self.game_display({"Red Points" : self.red_points, "Blue Points" : self.blue_points})
        self.set_starting_player()
        self.create_border(self.current_player)

    def game_loop(self) -> None:
        while self.can_play:
            position = int(self.uart.read())
            self.update_board(position)
