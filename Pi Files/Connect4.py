from GameClass import Game
from time import sleep
from random import randint

class Connect4(Game):
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, font2 = None, uart = None) -> None:
        super().__init__(leds, display, image, draw, font, font2)
        self.uart = uart
        self.current_player = None
        self.red_points = 0
        self.blue_points = 0
        self.GAME_ROWS = 7
        self.GAME_COLUMNS = 7
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
        position = (position % self.COLUMNS) + (self.ROWS + self.ROWS) # modulate the add two rows to be in area

        if self.leds[position] == self.DIM_WHITE:
            for i in range(0, self.GAME_ROWS):
                self.leds[position] = self.current_player

                if i < (self.COLUMNS - 2) and self.leds[position + self.ROWS] == self.DIM_WHITE:
                    sleep(0.05)
                    self.leds[position] = self.DIM_WHITE
                    position += self.ROWS
        
            self.check_win(position)

        else:
            print("position:", position, "is already taken")

    def create_border(self, color : list) -> None:
        positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 31, 32, 33, 34, 42, 43, 44, 45, 53, 54, 55, 56, 64, 65, 66, 67, 75, 76, 77, 78, 86, 87, 88, 89, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
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
        print("winning positions:", winning_positions)
        for i in winning_positions:
            self.leds[i] = [0, 255, 0]
            sleep(0.1)

    def is_row_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            scan_position = position + i
#             if scan_position % self.COLUMNS == 2:
#                 break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break
            
        for i in range(1, 4):
            scan_position = position - i
#             if scan_position % self.COLUMNS == 9:
#                 break

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
            scan_position = position + (i * self.COLUMNS)
#             if scan_position > 96:
#                 break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
        
        return False


    def is_diag_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            print("Position: ", position)
            scan_position = position + (i * self.COLUMNS) + i
            print("scanned  position:", scan_position)
#             if scan_position > 96 or scan_position % self.GAME_COLUMNS == 2:
#                 break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
            scan_position = position - (i * self.COLUMNS) - i #96, 84, 81, 67
#             if scan_position < 24 or scan_position % self.GAME_COLUMNS == 10:
#                 break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        if len(winning_positions) >= 4:
            self.show_win(winning_positions)
            return True
    
        winning_positions = [position]

        for i in range(1, 4):
            scan_position = position + (i * self.COLUMNS) - i
#             if scan_position > 96 or scan_position % self.COLUMNS == 10:
#                 break

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
            scan_position = position - (i * self.COLUMNS) + i
#             if scan_position < 24 or scan_position % self.COLUMNS == 2:
#                 break

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
        self.leds.fill(self.DIM_WHITE)
        self.game_display()
        self.update_score()
        self.set_starting_player()
        self.leds.show()
        self.leds.auto_write = True

    def main_loop(self) -> None:
        while self.can_play:
            #print(self.uart.isOpen())
            #self.uart.flushInput()
            position = self.uart.readline()
#             print(self.uart.isOpen())
#             print(position)
            
            if position:
#                 print(int(position))
                self.update_board(int(position))
#             else:
#                  sleep(0.1)
                 #print("connect 4 uart timed out, trying again...")
                
        self.finished = True

