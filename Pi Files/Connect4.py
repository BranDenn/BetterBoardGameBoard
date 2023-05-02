from GameClass import Game
from time import sleep
from random import randint
import json

class Connect4(Game):
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, font2 = None, uart = None, save_sel = 0, last_file_number = 0) -> None:
        super().__init__(leds, display, image, draw, font, font2)
        self.uart = uart
        self.current_player = None
        self.red_points = 0
        self.blue_points = 0
        self.save_sel = save_sel
        
        print('SAVE SEL:' , save_sel)
        print("Nuum:", last_file_number)
        if save_sel > 0:
            self.file_location = "/home/b1128c/BetterBoardGameBoard/Pi Files/saves/save %d.json" % save_sel
        else:
            self.file_location = "/home/b1128c/BetterBoardGameBoard/Pi Files/saves/save %d.json" % (last_file_number + 1)
            
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
            for i in range(0, self.ROWS - 4):
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
        self.play_win_sound()
        for i in winning_positions:
            self.leds[i] = [0, 255, 0]
            sleep(0.1)

    def is_row_win(self, position : int) -> bool:
        winning_positions = [position]
        scan_position = 0

        for i in range(1, 4):
            scan_position = position + i

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break
            
        for i in range(1, 4):
            scan_position = position - i

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
            scan_position = position + (i * self.COLUMNS) + i

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
            scan_position = position - (i * self.COLUMNS) - i

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

            if self.leds[scan_position] == self.current_player:
                winning_positions.append(scan_position)
            else:
                break

        for i in range(1, 4):
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
            self.start_game(True)

        elif self.DIM_WHITE not in self.leds:
            self.create_border([255, 127, 0])
            sleep(2.5)
            self.start_game(True)

        else:
            self.next_player()
            self.save_game()
        
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

    def save_game(self) -> None:
        board = [pos for pos in self.leds]
        
        with open(self.file_location, 'w') as f:
            json.dump({"Current Player" : self.current_player,
                      "Red Points" : self.red_points,
                      "Blue Points" : self.blue_points,
                      "LED Data" : board}, f, indent = 4)
            
        print("file saved: " + self.file_location)
    
    def load_save(self) -> None:
        with open(self.file_location, 'r') as f:
            data = json.load(f)
            
        self.current_player = data["Current Player"]
        self.red_points = data["Red Points"]
        self.blue_points = data["Blue Points"]
        
        for i in range(0, len(data["LED Data"])):
            self.leds[i] = data["LED Data"][i]
        
        print("file loaded:")
        
    def start_game(self, is_started = False) -> None:
        self.leds.auto_write = False
        
        if self.save_sel > 0 and not is_started:
            self.load_save()
        else:
            self.leds.fill(self.DIM_WHITE)
            self.set_starting_player()
            
        self.game_display()
        self.update_score()
        self.leds.show()
        self.leds.auto_write = True
        self.save_game()

    def main_loop(self) -> None:
        while self.can_play:
            position = self.uart.readline()

            if position:
                self.update_board(int(position))

        self.finished = True

