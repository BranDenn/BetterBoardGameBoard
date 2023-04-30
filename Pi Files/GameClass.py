class Game():
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None, font2 = None) -> None:
        self.can_play = True
        self.leds = leds
        self.disp = display
        self.img = image
        self.draw = draw
        self.font = font
        self.font2 = font2
        self.finished = False
        self.ROWS = 11
        self.COLUMNS = 11
        self.OFF = [0, 0, 0]
        self.RED = [255, 0, 0]
        self.BLUE = [0, 0, 255]
        self.WHITE = [255, 255, 255]

    def __del__(self) -> None:
        print(self.__class__.__name__, "has been destructed!")
        
    def clear_board(self) -> None:
        self.leds.auto_write = False
        self.leds.fill(self.OFF)
        self.leds.show()
        self.leds.auto_write = True
        
    def game_display(self) -> None:
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), fill = (255, 255, 255))
        self.draw.rectangle((0, 0, self.disp.width, 30), fill = (0, 0, 255))
        self.draw.rectangle((0, self.disp.height - 30, self.disp.width, self.disp.height), fill = (0, 0, 255))
        self.draw.text((self.disp.width * (1/2) - (self.font.getlength(self.__class__.__name__) / 2), 12), self.__class__.__name__, font = self.font, fill = (255, 255, 255))
        
        self.draw.text((5, 135), ("Hold Button to"), font = self.font, fill = (255, 255, 255))
        self.draw.text((5, 145), ("return to menu."), font = self.font, fill = (255, 255, 255))
        self.disp.display(self.img)