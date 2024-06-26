import tkinter as tk
import time
import random
import sys
import math
####################################################################################################################
# game parameters
# game window
snake_window = tk.Tk()
# game window size
win_x, win_y = 800, 800
game_window_dimensions = [win_x, win_y]
snake_window.geometry(str(win_x) + "x" + str(win_y))
# block game window size
snake_window.resizable(0, 0)
# window title
snake_window.title("Snake")
# close game window
snake_window.protocol("WM_DELETE_WINDOW", sys.exit)
# game window: bd - background; highlightthickness - frame
snake_canvas = tk.Canvas(snake_window, width=win_x, height=win_y, bd=0, highlightthickness=0)
snake_canvas.pack()
# snake segment size
snake_scale = 25
game_dimensions = [win_x // snake_scale, win_y // snake_scale]
# snake head - start postition, snake tail list
snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
snake_tail = []

snake2_coords = [(game_dimensions[0] // 2)+2, (game_dimensions[1] // 2)+2]
snake2_tail = []
# snake movement direction[x,y]
snake_move_dir = [1, 0]
snake2_move_dir = [1, 0]

snake_moved_in_this_frame = False
snake2_moved_in_this_frame = False
# frames per second
wps = 10
####################################################################################################################
# GAME FUNCTIONS
####################################################################################################################
# fill game field grid
def createGridItem(coords, hexcolor):
    snake_canvas.create_rectangle((coords[0]) * snake_scale, (coords[1]) * snake_scale, (coords[0] + 1) * snake_scale,
                                 (coords[1] + 1) * snake_scale, fill=hexcolor, outline="#222222", width=3)

# apple coordinates
def generateAppleCoords():
    # use snake tail
    global snake_tail
    # apple coordinates
    apple_coords = [random.randint(0, (game_dimensions[0] - 1)), random.randint(0, (game_dimensions[1] - 1))]
    # apple may not be a part of snake tail
    for segment in snake_tail:
        if (segment[0] == apple_coords[0] and segment[1] == apple_coords[1]):
            return generateAppleCoords()
    # apple coordinates
    return apple_coords

restart_window_open = False
winner_window = None

def show_winner(winner):
    global restart_window_open, winner_window
    if not restart_window_open:
        winner_window = tk.Toplevel(snake_window)
        winner_window.title("Game Over")
        winner_label = tk.Label(winner_window, text=f"Snake {winner} wins!", font=("Helvetica", 20))
        winner_label.pack(pady=20)
        restart_button = tk.Button(winner_window, text="Restart Game", command=restart_game)
        restart_button.pack(pady=10)
        restart_window_open = True

def restart_game():
    global snake_coords, snake_tail, snake2_coords, snake2_tail, snake_move_dir, snake2_move_dir, apple_coords, restart_window_open, winner_window
    if winner_window:
        winner_window.destroy()
    snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
    snake_tail = []
    snake2_coords = [(game_dimensions[0] // 2) + 2, (game_dimensions[1] // 2) + 2]
    snake2_tail = []
    snake_move_dir = [1, 0]
    snake2_move_dir = [1, 0]
    apple_coords = generateAppleCoords()
    restart_window_open = False



# game
def gameloop():
    # global game variables
    global wps
    global snake_moved_in_this_frame
    global snake2_moved_in_this_frame
    global snake_canvas
    global game_dimensions
    global window_dimensions
    global snake_tail
    global snake_coords
    global snake2_tail
    global snake2_coords
    global snake_move_dir
    global snake2_move_dir
    global apple_coords
    global restart_window_open  

    if restart_window_open:  # Check if restart window is open
        return  # If restart window is open, do not update game state

    # game speed =  1s/wps (frames per second)
    snake_window.after(1000 // wps, gameloop)
    # clear game window
    snake_canvas.delete("all")
    # set background
    snake_canvas.create_rectangle(0, 0, win_x, win_y, fill="#222222", outline="#222222")

    # add the snake head
    snake_tail.append([snake_coords[0], snake_coords[1]])
    snake2_tail.append([snake2_coords[0], snake2_coords[1]])
    
    # move the snake1
    snake_coords[0] += snake_move_dir[0]
    snake_coords[1] += snake_move_dir[1]
    
    if (snake_coords[0] == game_dimensions[0] or snake_coords[0] == -1 or snake_coords[1] == game_dimensions[1] or snake_coords[1] == -1):
        show_winner('Red')
        return
                
    # move the snake 2
    snake2_coords[0] += snake2_move_dir[0]
    snake2_coords[1] += snake2_move_dir[1]
    
    if (snake2_coords[0] == game_dimensions[0] or snake2_coords[0] == -1 or snake2_coords[1] == game_dimensions[1] or snake2_coords[1] == -1):
        show_winner('Green')
        return
        
    # snake moved in the frame
    snake_moved_in_this_frame = False
    snake2_moved_in_this_frame = False

    # head-tail and other snake collision - game restart
    for segment in snake_tail:
        if (segment[0] == snake_coords[0] and segment[1] == snake_coords[1]):
            snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
            snake_tail = []
            snake2_coords = [(game_dimensions[0] // 2)+2, (game_dimensions[1] // 2)+2]
            snake2_tail = []
            snake_move_dir = [1, 0]
            snake2_move_dir = [1, 0]
            apple_coords = generateAppleCoords()

        if (segment[0] == snake2_coords[0] and segment[1] == snake2_coords[1]):
            snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
            snake_tail = []
            snake2_coords = [(game_dimensions[0] // 2)+2, (game_dimensions[1] // 2)+2]
            snake2_tail = []
            snake_move_dir = [1, 0]
            snake2_move_dir = [1, 0]
            apple_coords = generateAppleCoords()

        # display a snake
        createGridItem(segment, "#00ff00")
        
    # head-tail collision 2 - game restart
    for segment in snake2_tail:
        if (segment[0] == snake_coords[0] and segment[1] == snake_coords[1]):
            snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
            snake_tail = []
            snake2_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
            snake2_tail = []
            snake_move_dir = [1, 0]
            snake2_move_dir = [1, 0]
            apple_coords = generateAppleCoords()
            
        if (segment[0] == snake2_coords[0] and segment[1] == snake2_coords[1]):
            snake_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
            snake_tail = []
            snake2_coords = [game_dimensions[0] // 2, game_dimensions[1] // 2]
            snake2_tail = []
            snake_move_dir = [1, 0]
            snake2_move_dir = [1, 0]
            apple_coords = generateAppleCoords()
        # display a snake
        createGridItem(segment, "#ff0000")

    # display an apple
    createGridItem(apple_coords, "#ff0000")
    # if an apple was eaten add one segment to the snake tail
    if (apple_coords[0] == snake_coords[0] and apple_coords[1] == snake_coords[1]):
        apple_coords = generateAppleCoords()
    else:
        snake_tail.pop(0)
        
    # if an apple was eaten add one segment to the snake tail 2
    if (apple_coords[0] == snake2_coords[0] and apple_coords[1] == snake2_coords[1]):
        apple_coords = generateAppleCoords()
    else:
        snake2_tail.pop(0)

# keyboard
def key(e):
    # global variables used
    global snake_move_dir
    global snake2_move_dir
    global snake_moved_in_this_frame
    global snake2_moved_in_this_frame

    # check if snake moved in this frame
    if (snake_moved_in_this_frame == False):
        snake_moved_in_this_frame = True

        # arrow keys
        if (e.keysym == "Left" and snake_move_dir[0] != 1):
            snake_move_dir  = [-1, 0]
        elif (e.keysym == "Right" and snake_move_dir[0] != -1):
            snake_move_dir  = [1, 0]
        elif (e.keysym == "Up" and snake_move_dir[1] != 1):
            snake_move_dir  = [0, -1]
        elif (e.keysym == "Down" and snake_move_dir[1] != -1):
            snake_move_dir  = [0, 1]

    # check if snake moved in this frame
    if (snake2_moved_in_this_frame == False):
        snake2_moved_in_this_frame = True
        if e.keysym == "a" and snake2_move_dir[0] != 1:
            snake2_move_dir = [-1, 0]
        elif e.keysym == "d" and snake2_move_dir[0] != -1:
            snake2_move_dir = [1, 0]
        elif e.keysym == "w" and snake2_move_dir[1] != 1:
            snake2_move_dir = [0, -1]
        elif e.keysym == "s" and snake2_move_dir[1] != -1:
            snake2_move_dir = [0, 1]
        else:
            snake2_moved_in_this_frame = False
 
            
            
####################################################################################################################
# place an apple
apple_coords = generateAppleCoords()
# binding function
snake_window.bind("<KeyPress>", key)
# game
gameloop()
# display game window and check for keyboard event
snake_window.mainloop()
