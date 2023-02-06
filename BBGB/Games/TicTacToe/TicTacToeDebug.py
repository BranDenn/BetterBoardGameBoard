import tkinter # GUI library
import customtkinter # Modern tkinter GUI library extention
import random # used to randomize first player turn
from pyglet import media # used to output sounds
#import RPi.GPIO as GPIO
#import board?
#import neopixel

#LEDstrip = neopixel.NeoPixel(board.D18, 9, brightness = 1)

# TICTACTOE VARS
player = '' # declare player as character
board = [] # declare board as array

winSound = media.load('Sounds\YayWin.wav', streaming = False) # create sounds for winning
oSound = media.load('Sounds\Button_01.wav', streaming = False) # create sounds for player turns
xSound = media.load('Sounds\Button_02.wav', streaming = False)
# ------------------------------------------

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("blue")  #Themes: blue (default), dark-blue, green

app = customtkinter.CTk() # create customtkinter gui app window
app.title("TicTacToe Debug") # give name to app
app.geometry("432x496") # define app dimensions
app.resizable(False, False) # disable the ability to resize the window

label = customtkinter.CTkLabel(master = app, font = ("Arial", 64)) # create a label used to notify player turns
label.place(relx=0.5, rely=1.0, anchor=tkinter.S) # place label at the bottom of the app

def update_board(position) -> None: # updates board position with player data
  board[position] = player
    
  if player == 'o': # updates position colors and disable button
    app.winfo_children()[position + 1].configure(fg_color = "blue", state = "disabled", text = "o") # turns pressed button to player color (o = blue) and disables button
    oSound.play() # play o player sound
    #LEDstrip[position] = (0, 0, 255)
  else:
    app.winfo_children()[position + 1].configure(fg_color = "red", state = "disabled", text = "x") # turns pressed button to player color (x = red) and disables button
    xSound.play() # play x player sound
    #LEDstrip[position] = (255, 0, 0)

  check_win()
  
def create_buttons() -> None: # creates 3x3 grid with their own position ID
  offset = 0 # declare offeset to give each button a unique position

  for row in range(3): # for each row in tic-tac-toe
    for col in range(3): # for each column in that row

      def button_function(x = row + col + offset): # create a function for that each tic-tac-toe cell will correspond to
        # the offset will give approprate values to correspond to array (row 2, column 2) should be cell 4 (5 - 1 for array), but without offset it would be 3
        return update_board(x)

      # create a button that links to its appropritate function created above
      btn = customtkinter.CTkButton(master = app,
                                    hover_color = "gray",
                                    text = "",
                                    command = button_function,
                                    width = 128,
                                    height = 128,
                                    font = ("Arial", 96)
                                    ) 
      btn.grid(row = row, column = col, sticky = "nsew", padx = 8, pady = 8)

    offset += 2 # add 2 to offset to account for next row (3 - 1 for array)

def update_label(s: str) -> None: # sets notifcation label with text
  label.configure(text = s)

def start() -> None: # initializes the board
  global board # get the global board variable to update
  global player # get the global player variable to update

  board = [''] * 9 # clears board 
  # ['', '', '', 
  #  '', '', '',
  #  '', '', '']
  #LEDstrip.fill((50, 50, 50))

  for i in range(1, 10): # loop through all buttons created (the range starts at 1 since the label counts as child 0)
    app.winfo_children()[i].configure(fg_color = "black", state = "normal", text = "")  # initialize every button back to normal so that it can be pressed again

  rand_player = random.randint(0, 1) # randomly select player
  if rand_player == 0: # 50 % chance start with player 'o'
    player = 'o'
  else:  # 50 % chance start with player 'x'
    player = 'x'

  update_label(player + "'s turn!") # show the player's turn on the notification label

def next_player() -> None: # set next player (same as player initialization, but without random player)
  global player

  if player == 'o':
    player = 'x'
  else:
    player = 'o'

  update_label(player + "'s turn!")

def set_button_win_color(positions : list) -> None: # set the winning button colors to white to clearly indicate the win
  app.winfo_children()[positions[0] + 1].configure(fg_color = "white")
  app.winfo_children()[positions[1] + 1].configure(fg_color = "white")
  app.winfo_children()[positions[2] + 1].configure(fg_color = "white")
  #LEDstrip[positions[0]] = (255, 255, 255)
  #LEDstrip[positions[1]] = (255, 255, 255)
  #LEDstrip[positions[2]] = (255, 255, 255)

def check_row() -> bool: # check row win
  if board[0] == player and board[1] == player and board[2] == player: # if first row is all the same player
    set_button_win_color([0, 1, 2]) # indicate win
    return True

  if board[3] == player and board[4] == player and board[5] == player: # if second row is all the same player
    set_button_win_color([3, 4, 5]) # indicate win
    return True

  if board[6] == player and board[7] == player and board[8] == player: # if third row is all the same player
    set_button_win_color([6, 7, 8]) # indicate win
    return True

  return False

def check_col() -> bool: # check col win
  if board[0] == player and board[3] == player and board[6] == player: # if first column is all the same player
    set_button_win_color([0, 3, 6]) # indicate win
    return True

  if board[1] == player and board[4] == player and board[7] == player: # if first column is all the same player
    set_button_win_color([1, 4, 7]) # indicate win
    return True

  if board[2] == player and board[5] == player and board[8] == player: # if first column is all the same player
    set_button_win_color([2, 5, 8]) # indicate win
    return True

  return False

def check_diag() -> bool: # check diag win
  if board[0] == player and board[4] == player and board[8] == player: # if diagnal (top left to bottom right) is all the same player
    set_button_win_color([0, 4, 8]) # indicate win
    return True

  if board[2] == player and board[4] == player and board[6] == player: # if diagnal (top right to bottom left) is all the same player
    set_button_win_color([2, 4, 6]) # indicate win
    return True

  return False

def check_win() -> None:
  if check_row() or check_col() or check_diag(): # checks all cases for player to win
    for i in range(1, 10): # if player wins make sure no buttons can pressed (prevents errors after game is supposed to be over)
      app.winfo_children()[i].configure(state = "disabled")
    update_label(player + " wins!") # update notification label to show winner
    winSound.play() # play win sound
    label.after(1500, start)  # restart the game after 1.5s

  elif '' not in board: # checks if all spots are taken up and no one has won
    update_label("DRAW!") # update notification label to show draw
    label.after(1500, start)  # restart after game after 1.5s

  else: # if no one has won and the board is not full, go to next players turn
    next_player()

if __name__ == "__main__":
  create_buttons() # create buttons first (gui for tic-tac-toe board)
  start() # start the game
  app.mainloop() # allow tkinter gui to show and run
