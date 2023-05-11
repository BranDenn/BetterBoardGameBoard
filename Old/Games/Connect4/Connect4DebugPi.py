import tkinter # GUI library
import customtkinter # Modern tkinter GUI library extention
import random # used to randomize first player turn
from pygame import mixer
from time import sleep
import board
import digitalio
import neopixel

# 21 for no pwm interference
LEDstrip = neopixel.NeoPixel(board.D21, 66, brightness = 0.25)

# Pins to toggle interrupt
player1_PIN = digitalio.DigitalInOut(board.D16)
player1_PIN.direction = digitalio.Direction.OUTPUT

player2_PIN = digitalio.DigitalInOut(board.D20)
player2_PIN.direction = digitalio.Direction.OUTPUT

LEDoffset = 2
#Inits for pygame audio
mixer.init()

win_sound = mixer.Sound("/home/b1128c/BetterBoardGameBoard/BBGB/Games/TicTacToe/Sounds/YayWin.wav")
p1_sound = mixer.Sound("/home/b1128c/BetterBoardGameBoard/BBGB/Games/TicTacToe/Sounds/Button_01.wav")
p2_sound = mixer.Sound("/home/b1128c/BetterBoardGameBoard/BBGB/Games/TicTacToe/Sounds/Button_02.wav")

# Need to declare the sound object that is being modified and then the value of the desired volume for the sound
mixer.Sound.set_volume(win_sound, 0.25)
mixer.Sound.set_volume(p1_sound, 0.10)
mixer.Sound.set_volume(p2_sound, 0.10)

# TICTACTOE VARS
ROW_COUNT = 6
COL_COUNT = 7

player = '' # declare player as character
board = [] # declare board as array

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("blue")  #Themes: blue (default), dark-blue, green

app = customtkinter.CTk() # create customtkinter gui app window
app.title("Connect 4 Debug") # give name to app
app.geometry("560x544") # define app dimensions
app.resizable(False, False) # disable the ability to resize the window

label = customtkinter.CTkLabel(master = app, font = ("Arial", 64)) # create a label used to notify player turns
label.place(relx=0.5, rely=1.0, anchor=tkinter.S) # place label at the bottom of the app

TIME = 0.05

def update_board(position) -> None: # updates board position with player data
    global LEDoffset
    
    position = position % COL_COUNT
    LEDoffset = 2
    
    if board[position] == '':
        for i in range(1, 43):
            app.winfo_children()[i].configure(state = "disabled")

        for i in range(ROW_COUNT):
            if player == 'Blue': # updates position colors and disable button
                app.winfo_children()[position + 1].configure(fg_color = "blue") # turns pressed button to player color (o = blue) and disables button
                LEDstrip[position + LEDoffset] = (0, 0, 255)
            else:
                app.winfo_children()[position + 1].configure(fg_color = "red") # turns pressed button to player color (x = red) and disables button
                LEDstrip[position + LEDoffset] = (255, 0, 0)
            app.update()

            if i < 5 and board[position + COL_COUNT] == '':
                mixer.Sound.play(p1_sound)
                sleep(TIME)
                app.winfo_children()[position + 1].configure(fg_color = "black")
                LEDstrip[position + LEDoffset] = (0, 0, 0)
                position += COL_COUNT
                LEDoffset += 4
                #mixer.Sound.play(p1_sound)
            else:
                break

        board[position] = player
        mixer.Sound.play(p2_sound)

        check_win(position)

    else:
        print("position already taken")

def create_buttons() -> None: # creates 3x3 grid with their own position ID
    offset = 0 # declare offeset to give each button a unique position

    for row in range(ROW_COUNT): # for each row in tic-tac-toe
        for col in range(COL_COUNT): # for each column in that row

            def button_function(x = row + col + offset): # create a function for that each tic-tac-toe cell will correspond to
                # the offset will give approprate values to correspond to array (row 2, column 2) should be cell 4 (5 - 1 for array), but without offset it would be 3
                return update_board(x)

            # create a button that links to its appropritate function created above
            btn = customtkinter.CTkButton(master = app,
                                            hover_color = "gray",
                                            text = "",
                                            command = button_function,
                                            width = 64,
                                            height = 64,
                                            ) 
            btn.grid(row = row, column = col, sticky = "nsew", padx = 8, pady = 8)

        offset += 6 # add 2 to offset to account for next row (3 - 1 for array)

def update_label(s: str) -> None: # sets notifcation label with text
  label.configure(text = s)

def start() -> None: # initializes the board
    global board # get the global board variable to update
    global player # get the global player variable to update

    board = [''] * 42 # clears board
    LEDstrip.fill((0, 0, 0))

    for i in range(1, 43): # loop through all buttons created (the range starts at 1 since the label counts as child 0)
        app.winfo_children()[i].configure(fg_color = "black", state = "normal")  # initialize every button back to normal so that it can be pressed again

    rand_player = random.randint(0, 1) # randomly select player
    if rand_player == 0: # 50 % chance start with player 'o'
        player = 'Blue'
    else:  # 50 % chance start with player 'x'
        player = 'Red'
    create_border()

    update_label(player + "'s turn!") # show the player's turn on the notification label

def create_border() -> None:
    if player == 'Blue':
        color = (0, 0, 20)
    else:
        color = (20, 0, 0)
        
    for i in range(ROW_COUNT):
        LEDstrip[0 + (i*11)] = color
        LEDstrip[1 + (i*11)] = color
        LEDstrip[9 + (i*11)] = color
        LEDstrip[10 + (i*11)] = color

def next_player() -> None: # set next player (same as player initialization, but without random player)
    global player

    if player == 'Blue':
        player = 'Red'
    else:
        player = 'Blue'
    create_border()

    update_label(player + "'s turn!")

def set_button_win_color(winning_positions : list) -> None: # set the winning button colors to white to clearly indicate the win
    for i in winning_positions:
        app.winfo_children()[i + 1].configure(fg_color = "white")
        
        for j in range(COL_COUNT):
            if i < (COL_COUNT * (j + 1)):
                LEDstrip[i + 2 + (j * 4)] = (0, 255, 0)
                break
            
    update_label(player + " connected %d!" % len(winning_positions)) # update notification label to show winner

    if player == 'Blue':
        player1_PIN.value = True
        player1_PIN.value = False
    else:
        player2_PIN.value = True
        player2_PIN.value = False

def check_row(position : int) -> bool: # check row win
    winning_positions = [position]
    check_position = 0

    for i in range(1, 4):
        check_position = position + i
        if check_position % COL_COUNT == 0:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    for i in range(1, 4):
        check_position = position - i
        if check_position % COL_COUNT == 6:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    if len(winning_positions) >= 4:
        set_button_win_color(winning_positions)
        print("win by row")
        return True

    return False

def check_col(position : int) -> bool: # check col win
    winning_positions = [position]
    check_position = 0

    for i in range(1, 4):
        check_position = position + (i * COL_COUNT)
        if check_position >= 42:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    for i in range(1, 4):
        check_position = position - (i * COL_COUNT)
        if check_position < 0:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    if len(winning_positions) >= 4:
        set_button_win_color(winning_positions)
        print("win by col")
        return True

    return False

def check_diag(position : int) -> bool: # check diag win
    winning_positions = [position]
    check_position = 0

    for i in range(1, 4):
        check_position = position + (i * COL_COUNT) + i
        if check_position >= 42 or check_position % COL_COUNT == 0:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    for i in range(1, 4):
        check_position = position - (i * COL_COUNT) - i
        if check_position < 0 or check_position % COL_COUNT == 6:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    if len(winning_positions) >= 4:
        set_button_win_color(winning_positions)
        print("win by diag1")
        return True

    winning_positions = [position]

    for i in range(1, 4):
        check_position = position + (i * COL_COUNT) - i
        if check_position >= 42 or check_position % COL_COUNT == 6:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    for i in range(1, 4):
        check_position = position - (i * COL_COUNT) + i
        if check_position < 0 or check_position % COL_COUNT == 0:
            break

        if board[check_position] == player:
            winning_positions.append(check_position)
        else:
            break

    if len(winning_positions) >= 4:
        set_button_win_color(winning_positions)
        print("win by diag2")
        return True

    return False

def check_win(position : int) -> None:
    if check_row(position) or check_col(position) or check_diag(position): # checks all cases for player to win
        for i in range(1, 43): # if player wins make sure no buttons can pressed (prevents errors after game is supposed to be over)
            app.winfo_children()[i].configure(state = "disabled")

        mixer.Sound.play(win_sound)
        label.after(2500, start)  # restart the game after 1.5s

    elif '' not in board: # checks if all spots are taken up and no one has won
        update_label("DRAW!") # update notification label to show draw
        LEDstrip.fill((255, 127, 0))
        label.after(2500, start)  # restart after game after 1.5s

    else: # if no one has won and the board is not full, go to next players turn
        next_player()
        for i in range(1, 43):
            app.winfo_children()[i].configure(state = "normal")

if __name__ == "__main__":
    create_buttons() # create buttons first (gui for tic-tac-toe board)
    start() # start the game
    app.mainloop() # allow tkinter gui to show and run
