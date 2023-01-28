import tkinter
import customtkinter
import random

# TICTACTOE VARS
player = ''
board = []
# TICTACTOE VARS

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
#customtkinter.set_default_color_theme("blue")  #Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("TicTacToe Debug")
app.geometry("432x496")
app.resizable(False, False)

label = customtkinter.CTkLabel(master = app, font = ("Arial", 64))
label.place(relx=0.5, rely=1.0, anchor=tkinter.S)

def update_board(position) -> None: # updates board position with player data
  board[position] = player
    
  if player == 'o': # updates position colors and disable button
    app.winfo_children()[position + 1].configure(fg_color = "blue", state = "disabled", text = "o")
  else:
    app.winfo_children()[position + 1].configure(fg_color = "red", state = "disabled", text = "x")

  check_win()
  
def create_buttons() -> None: # creates 3x3 grid with their own position ID
  offset = 0

  for row in range(3):
    for col in range(3):

      def button_function(x = row + col + offset): # each has its own function with position ID
        return update_board(x)

      btn = customtkinter.CTkButton(master = app,
                                    hover_color = "gray",
                                    text = "",
                                    command = button_function,
                                    width = 128,
                                    height = 128,
                                    font = ("Arial", 96)
                                    )
      btn.grid(row = row, column = col, sticky = "nsew", padx = 8, pady = 8)

    offset += 2

def update_label(s: str) -> None: # sets notifcation label with text
  label.configure(text = s)

def start() -> None: # initializes the board
  global board
  global player

  board = [''] * 9 # clears board

  for i in range(1, 10):
    app.winfo_children()[i].configure(fg_color = "black", state = "normal", text = "")

  rand_player = random.randint(0, 1) # randomly select player
  if rand_player == 0:
    player = 'o'
  else:
    player = 'x'

  update_label(player + "'s turn!")

def next_player() -> None: # set next player
  global player

  if player == 'o':
    player = 'x'
  else:
    player = 'o'

  update_label(player + "'s turn!")

def set_button_win_color(positions : list) -> None:
  app.winfo_children()[positions[0] + 1].configure(fg_color = "yellow")
  app.winfo_children()[positions[1] + 1].configure(fg_color = "yellow")
  app.winfo_children()[positions[2] + 1].configure(fg_color = "yellow")

def check_row() -> bool: # check row win
  if board[0] == player and board[1] == player and board[2] == player:
    set_button_win_color([0, 1, 2])
    return True

  if board[3] == player and board[4] == player and board[5] == player:
    set_button_win_color([3, 4, 5])
    return True

  if board[6] == player and board[7] == player and board[8] == player:
    set_button_win_color([6, 7, 8])
    return True

  return False

def check_col() -> bool: # check col win
  if board[0] == player and board[3] == player and board[6] == player:
    set_button_win_color([0, 3, 6])
    return True

  if board[1] == player and board[4] == player and board[7] == player:
    set_button_win_color([1, 4, 7])
    return True

  if board[2] == player and board[5] == player and board[8] == player:
    set_button_win_color([2, 5, 8])
    return True

  return False

def check_diag() -> bool: # check diag win
  if board[0] == player and board[4] == player and board[8] == player:
    set_button_win_color([0, 4, 8])
    return True

  if board[2] == player and board[4] == player and board[6] == player:
    set_button_win_color([2, 4, 6])
    return True

  return False

def check_win() -> None:
  if check_row() or check_col() or check_diag(): # checks all cases for player to win
    for i in range(1, 10):
      app.winfo_children()[i].configure(state = "disabled")
    update_label(player + " wins!")
    label.after(1500, start)  # restart after 1.5s

  elif '' not in board: # checks if all spots are taken up and no one has won
    update_label("DRAW!")
    label.after(1500, start)  # restart after 1.5s

  else: # if no one has won and the board is not full, go to next players turn
    next_player()

def main() -> None:
  create_buttons()
  start()
  app.mainloop()

if __name__ == "__main__":
  main()
