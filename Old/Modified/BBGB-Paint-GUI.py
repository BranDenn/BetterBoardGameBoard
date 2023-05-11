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
pi = True

if pi:
    import board # PI board library for GPIO pins
    import neopixel # neopixel library for LED strip

    # Init LEDs
    LEDstrip = neopixel.NeoPixel(board.D21, ROW_COUNT * COL_COUNT, brightness = 1.0)

else:
    # blank strip if PC only - not useful but allows for simpler code
    LEDstrip = [None] * (ROW_COUNT * COL_COUNT)

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("dark")

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
    for i in range(len(LEDstrip)):
        if LEDstrip[i] != [0, 0, 0] and LEDstrip[i] != None:
            print("LEDstrip[%d] =" % i, LEDstrip[i])

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

# example mario hardcode output
'''
LEDstrip[1] = (255, 88, 90)
LEDstrip[2] = (255, 88, 90)
LEDstrip[3] = (255, 88, 90)
LEDstrip[4] = (255, 88, 90)
LEDstrip[5] = (255, 88, 90)
LEDstrip[6] = (255, 88, 90)
LEDstrip[11] = (255, 88, 90)
LEDstrip[12] = (255, 88, 90)
LEDstrip[13] = (255, 88, 90)
LEDstrip[14] = (255, 88, 90)
LEDstrip[15] = (255, 88, 90)
LEDstrip[16] = (255, 88, 90)
LEDstrip[17] = (255, 88, 90)
LEDstrip[18] = (255, 88, 90)
LEDstrip[19] = (255, 88, 90)
LEDstrip[20] = (255, 88, 90)
LEDstrip[22] = (135, 106, 97)
LEDstrip[23] = (135, 106, 97)
LEDstrip[24] = (135, 106, 97)
LEDstrip[25] = (221, 206, 165)
LEDstrip[26] = (221, 206, 165)
LEDstrip[27] = (104, 106, 97)
LEDstrip[28] = (221, 206, 165)
LEDstrip[33] = (221, 206, 165)
LEDstrip[34] = (135, 106, 97)
LEDstrip[35] = (221, 206, 165)
LEDstrip[36] = (221, 206, 165)
LEDstrip[37] = (221, 206, 165)
LEDstrip[38] = (104, 106, 97)
LEDstrip[39] = (221, 206, 165)
LEDstrip[40] = (221, 206, 165)
LEDstrip[41] = (221, 206, 165)
LEDstrip[44] = (221, 206, 165)
LEDstrip[45] = (135, 106, 97)
LEDstrip[46] = (135, 106, 97)
LEDstrip[47] = (221, 206, 165)
LEDstrip[48] = (221, 206, 165)
LEDstrip[49] = (221, 206, 165)
LEDstrip[50] = (104, 106, 97)
LEDstrip[51] = (221, 206, 165)
LEDstrip[52] = (221, 206, 165)
LEDstrip[53] = (221, 206, 165)
LEDstrip[55] = (135, 106, 97)
LEDstrip[56] = (221, 206, 165)
LEDstrip[57] = (221, 206, 165)
LEDstrip[58] = (221, 206, 165)
LEDstrip[59] = (221, 206, 165)
LEDstrip[60] = (104, 106, 97)
LEDstrip[61] = (104, 106, 97)
LEDstrip[62] = (104, 106, 97)
LEDstrip[63] = (104, 106, 97)
LEDstrip[66] = (221, 206, 165)
LEDstrip[67] = (221, 206, 165)
LEDstrip[68] = (221, 206, 165)
LEDstrip[69] = (221, 206, 165)
LEDstrip[70] = (221, 206, 165)
LEDstrip[71] = (221, 206, 165)
LEDstrip[72] = (221, 206, 165)
LEDstrip[73] = (221, 206, 165)
LEDstrip[77] = (255, 88, 90)
LEDstrip[78] = (255, 88, 90)
LEDstrip[79] = (114, 160, 214)
LEDstrip[80] = (255, 88, 90)
LEDstrip[81] = (255, 88, 90)
LEDstrip[82] = (255, 88, 90)
LEDstrip[83] = (255, 88, 90)
LEDstrip[84] = (255, 88, 90)
LEDstrip[88] = (255, 88, 90)
LEDstrip[89] = (255, 88, 90)
LEDstrip[90] = (114, 160, 214)
LEDstrip[91] = (255, 88, 90)
LEDstrip[92] = (255, 88, 90)
LEDstrip[93] = (255, 88, 90)
LEDstrip[94] = (114, 160, 214)
LEDstrip[95] = (255, 88, 90)
LEDstrip[96] = (255, 88, 90)
LEDstrip[99] = (255, 88, 90)
LEDstrip[100] = (255, 88, 90)
LEDstrip[101] = (114, 160, 214)
LEDstrip[102] = (114, 160, 214)
LEDstrip[103] = (114, 160, 214)
LEDstrip[104] = (114, 160, 214)
LEDstrip[105] = (114, 160, 214)
LEDstrip[106] = (255, 88, 90)
LEDstrip[107] = (255, 88, 90)
LEDstrip[108] = (255, 88, 90)
LEDstrip[109] = (255, 88, 90)
LEDstrip[110] = (255, 88, 90)
LEDstrip[111] = (255, 88, 90)
LEDstrip[112] = (114, 160, 214)
LEDstrip[113] = (114, 160, 214)
LEDstrip[114] = (114, 160, 214)
LEDstrip[115] = (114, 160, 214)
LEDstrip[116] = (114, 160, 214)
LEDstrip[117] = (255, 88, 90)
LEDstrip[118] = (255, 88, 90)
LEDstrip[119] = (255, 88, 90)
LEDstrip[120] = (255, 88, 90)
'''

# example house hardcode output
'''
LEDstrip[18] = (70, 255, 82)
LEDstrip[19] = (70, 255, 82)
LEDstrip[20] = (70, 255, 82)
LEDstrip[25] = (245, 72, 80)
LEDstrip[29] = (70, 255, 82)
LEDstrip[30] = (70, 255, 82)
LEDstrip[31] = (70, 255, 82)
LEDstrip[35] = (245, 72, 80)
LEDstrip[36] = (245, 72, 80)
LEDstrip[37] = (245, 72, 80)
LEDstrip[40] = (70, 255, 82)
LEDstrip[41] = (162, 99, 82)
LEDstrip[42] = (70, 255, 82)
LEDstrip[45] = (245, 72, 80)
LEDstrip[46] = (245, 72, 80)
LEDstrip[47] = (245, 72, 80)
LEDstrip[48] = (245, 72, 80)
LEDstrip[49] = (245, 72, 80)
LEDstrip[52] = (162, 99, 82)
LEDstrip[56] = (245, 72, 80)
LEDstrip[57] = (245, 72, 80)
LEDstrip[58] = (146, 103, 82)
LEDstrip[59] = (245, 72, 80)
LEDstrip[60] = (245, 72, 80)
LEDstrip[63] = (162, 99, 82)
LEDstrip[65] = (117, 238, 112)
LEDstrip[67] = (78, 102, 107)
LEDstrip[68] = (78, 102, 107)
LEDstrip[69] = (146, 103, 82)
LEDstrip[70] = (78, 102, 107)
LEDstrip[71] = (78, 102, 107)
LEDstrip[73] = (117, 238, 112)
LEDstrip[74] = (117, 238, 112)
LEDstrip[75] = (117, 238, 112)
LEDstrip[76] = (117, 238, 112)
LEDstrip[77] = (117, 238, 112)
LEDstrip[78] = (117, 238, 112)
LEDstrip[79] = (117, 238, 112)
LEDstrip[80] = (117, 238, 112)
LEDstrip[81] = (117, 238, 112)
LEDstrip[82] = (117, 238, 112)
LEDstrip[83] = (117, 238, 112)
LEDstrip[84] = (117, 238, 112)
LEDstrip[85] = (117, 238, 112)
LEDstrip[86] = (117, 238, 112)
LEDstrip[87] = (117, 238, 112)
LEDstrip[88] = (183, 151, 112)
LEDstrip[89] = (183, 151, 112)
LEDstrip[90] = (183, 151, 112)
LEDstrip[91] = (183, 151, 112)
LEDstrip[92] = (183, 151, 112)
LEDstrip[93] = (183, 151, 112)
LEDstrip[94] = (183, 151, 112)
LEDstrip[95] = (183, 151, 112)
LEDstrip[96] = (183, 151, 112)
LEDstrip[97] = (183, 151, 112)
LEDstrip[98] = (183, 151, 112)
LEDstrip[99] = (183, 151, 112)
LEDstrip[100] = (183, 151, 112)
LEDstrip[101] = (183, 151, 112)
LEDstrip[102] = (183, 151, 112)
LEDstrip[103] = (183, 151, 112)
LEDstrip[104] = (183, 151, 112)
LEDstrip[105] = (183, 151, 112)
LEDstrip[106] = (183, 151, 112)
LEDstrip[107] = (183, 151, 112)
LEDstrip[108] = (183, 151, 112)
LEDstrip[109] = (183, 151, 112)
LEDstrip[110] = (183, 151, 112)
LEDstrip[111] = (183, 151, 112)
LEDstrip[112] = (183, 151, 112)
LEDstrip[113] = (183, 151, 112)
LEDstrip[114] = (183, 151, 112)
LEDstrip[115] = (183, 151, 112)
LEDstrip[116] = (183, 151, 112)
LEDstrip[117] = (183, 151, 112)
LEDstrip[118] = (183, 151, 112)
LEDstrip[119] = (183, 151, 112)
'''

