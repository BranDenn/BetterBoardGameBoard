import tkinter # GUI library
import customtkinter # Modern tkinter GUI library extention
import random # Randomizer

# CONSTANT ROW and COL COUNTS
ROW_COUNT = 11
COL_COUNT = 11

# initial color values as tuple
color = (255, 255, 255)

# FALSE = PC ONLY
# TRUE = RASPBERRY PI
pi = False

if pi:
	import board # PI board library for GPIO pins
	import neopixel # neopixel library for LED strip

	# Init LEDs
	LEDstrip = neopixel.NeoPixel(board.D21, ROW_COUNT * COL_COUNT, brightness = 1.0)

else:
	# blank strip if PC only - not useful but allows for simpler code
	LEDstrip = [None] * (ROW_COUNT * COL_COUNT)

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("system")

# create customtkinter gui app window
app = customtkinter.CTk()

# give name to app
app.title("BBGB Paint")

# define app dimensions
app.geometry("618x718")

# prevent window resizing
app.resizable(False, False)

# grabs color from pixel as hex value and converts to rgb for global value
# this function is called from middle (MMB) clicking a button
# colors are updated when color is grabbed
def grab_color(position) -> None:
	global color
	hex = app.winfo_children()[position].cget("fg_color")
	# remove '#' from hex value
	hex = hex.lstrip('#')
	# convert h to rgb tuple
	color = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
	set_canvas()
	set_sliders()

# erases color from pixel
# this function is called from right (RMB) clicking a button
def clear_color(position) -> None:
	app.winfo_children()[position].configure(fg_color = "#000000")
	LEDstrip[position] = (0, 0, 0)

# erases all colors
def clear_all() -> None:
	for i in range(ROW_COUNT * COL_COUNT):
		app.winfo_children()[i].configure(fg_color = "#000000")
		LEDstrip[i] = (0, 0, 0)

# updates pixel with color
# GUI uses rgb to hex conversion
# LEDs use rgb
def update_board(position : int) -> None:
	app.winfo_children()[position].configure(fg_color = "#%02x%02x%02x" % color)
	LEDstrip[position] = color

# sets red value from slider
def set_r(r : float) -> None:
	global color
	color = (int(r), color[1], color[2])
	set_canvas()

# sets green value from slider
def set_g(g : float) -> None:
	global color
	color = (color[0], int(g), color[2])
	set_canvas()

# sets blue value from slider
def set_b(b : float) -> None:
	global color
	color = (color[0], color[1], int(b))
	set_canvas()

# generates a random color from button press
def set_random_color() -> None:
	global color
	color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	set_canvas()
	set_sliders()

# sets canvas color
def set_canvas() -> None:
	canvas.configure(bg = "#%02x%02x%02x" % color)

# sets sliders to correspond to color values
def set_sliders() -> None:
	red_slider.set(color[0])
	green_slider.set(color[1])
	blue_slider.set(color[2])

# prints LED code to be implemented in animation, etc.
def print_output() -> None:
	print("----- LED CODE -----")
	positions = []
	for i in range(len(LEDstrip)):
		if LEDstrip[i] != (0, 0, 0) and LEDstrip[i] != None:
			#print("self.leds[%d] =" % i, LEDstrip[i])
			#print("self.leds[%d] = self.get_random_color()" % i)
			positions.append(i)
	print(positions)

# creates buttons in a grid defined on the ROW and COL COUNT
# each button has its unique position
# they are also bounded to mouse buttons for extra functionality
def create_buttons() -> None: # creates 3x3 grid with their own position ID
	offset = 0

	for row in range(ROW_COUNT): # for each row in tic-tac-toe
		for col in range(COL_COUNT): # for each column in that row

			 # create a function for each button with proper position
			def button_function(x = row + col + offset):
				return update_board(x)
			
			# create a button that links to its appropritate function created above
			btn = customtkinter.CTkButton(master = app,
										text = "",
										width = 48,
										height = 48,
										fg_color = "#000000",
										hover_color = "gray",
										command = button_function
										)
			# binds for buttons to functions
			# lambda "event" is a default argument input and must written
			btn.bind("<Button-2>", command = lambda event, x = row + col + offset: grab_color(x))
			btn.bind("<Button-3>", command = lambda event, x = row + col + offset: clear_color(x))

			# grid the buttons
			btn.grid(row = row, column = col, sticky = "nsew", padx = 4, pady = 4)

		offset += 10

# create the buttons
create_buttons()

# slider for red value
red_slider = customtkinter.CTkSlider(app, from_=0, to=255, number_of_steps=255, 
			     progress_color="red", button_color="white", button_hover_color="gray", command=set_r)
red_slider.place(relx=0.5, rely=0.91, anchor=tkinter.S)

# slider for green value
green_slider = customtkinter.CTkSlider(app, from_=0, to=255, number_of_steps=255, 
			     progress_color="green", button_color="white", button_hover_color="gray", command=set_g)
green_slider.place(relx=0.5, rely=0.94, anchor=tkinter.S)

# slider for blue value
blue_slider = customtkinter.CTkSlider(app, from_=0, to=255, number_of_steps=255, 
			     progress_color="blue", button_color="white", button_hover_color="gray", command=set_b)
blue_slider.place(relx=0.5, rely=0.97, anchor=tkinter.S)

# canvas to display picked color
canvas = customtkinter.CTkCanvas(app, width = 64, height = 64, bg = "white")
canvas.place(relx=0.75, rely=0.97, anchor=tkinter.S)

# output button to generate the code output
output_button = customtkinter.CTkButton(master = app,
										text = "print output",
										text_color="black",
										width = 64,
										height = 64,
										fg_color = "white",
										hover_color = "gray",
										command = print_output
										) 
output_button.place(relx=0.91, rely=0.98, anchor=tkinter.S)

# random button to randomly pick a color
random_button = customtkinter.CTkButton(master = app,
										text = "random color",
										text_color = "black",
										width = 64,
										height = 64,
										fg_color = "white",
										hover_color = "gray",
										command = set_random_color
										) 
random_button.place(relx=0.23, rely=0.98, anchor=tkinter.S)

# clear all button to erase all colors
clear_button = customtkinter.CTkButton(master = app,
										text = "clear all",
										text_color = "black",
										width = 64,
										height = 64,
										fg_color = "white",
										hover_color = "gray",
										command = clear_all
										) 
clear_button.place(relx=0.09, rely=0.98, anchor=tkinter.S)

set_canvas()
set_sliders()

# main loop for app to run
app.mainloop()