from pygame import mixer

class Game():
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, font2 = None) -> None:
        self.can_play = True
        self.leds = leds
        self.disp = display
        self.img = image
        self.draw = draw
        self.font = font
        self.font2 = font2
        self.win_sound = mixer.Sound("/home/b1128c/BetterBoardGameBoard/Pi Files/audio/win.wav")
        self.finished = False
        self.ROWS = 11
        self.COLUMNS = 11
        self.OFF = [0, 0, 0]
        self.RED = [255, 0, 0]
        self.BLUE = [0, 0, 255]
        self.WHITE = [255, 255, 255]
        self.DIM_WHITE = [100,100,100]

    def __del__(self) -> None:
        print(self.__class__.__name__, "has been destructed!")
        
    def clear_board(self) -> None:
        self.leds.auto_write = False
        self.leds.fill(self.OFF)
        self.leds.show()
        self.leds.auto_write = True
        
    def play_win_sound(self) -> None:
        mixer.Sound.play(self.win_sound)

    def game_display(self, text_override : str or None = None) -> None:
        print("displaying game!")
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), fill = (255, 255, 255))
        self.draw.rectangle((0, 0, self.disp.width, 30), fill = (0, 0, 255))
        self.draw.rectangle((0, self.disp.height - 30, self.disp.width, self.disp.height), fill = (0, 0, 255))
        if text_override:
            self.draw.text((self.disp.width * (1/2) - (self.font.getlength(text_override) / 2), 12), text_override, font = self.font, fill = (255, 255, 255))
        else:
            self.draw.text((self.disp.width * (1/2) - (self.font.getlength(self.__class__.__name__) / 2), 12), self.__class__.__name__, font = self.font, fill = (255, 255, 255))
        
        self.draw.text((5, 135), ("Hold Button to"), font = self.font, fill = (255, 255, 255))
        self.draw.text((5, 145), ("return to menu."), font = self.font, fill = (255, 255, 255))
        self.disp.display(self.img)