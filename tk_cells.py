import tkinter as tk
import time
import numpy as np
from cell import Cells


# Static
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_WIDTH = 10

# Data
MOST_LEFT = CELL_WIDTH / 2
MOST_RIGHT = WINDOW_WIDTH - CELL_WIDTH / 2
MOST_TOP = CELL_WIDTH / 2
MOST_BOTTOM = WINDOW_HEIGHT - CELL_WIDTH / 2
CELL_NUM = 10

# TK
root = tk.Tk()

canvas = tk.Canvas(root, bg='white', width=800, height=600)
canvas.configure(bg='white')
canvas.pack(fill=tk.BOTH, expand=tk.YES)

X = np.random.randint( MOST_LEFT, MOST_RIGHT - CELL_WIDTH, CELL_NUM )
Y = np.random.randint( MOST_TOP, MOST_BOTTOM - CELL_WIDTH, CELL_NUM )
for x, y in zip(X, Y):
    rect_id = canvas.create_rectangle(x,y,x+CELL_WIDTH,y+CELL_WIDTH)
    print("id: " + str(rect_id))

# Function
def one_generation(event):
    global X
    global Y
    print("Do one generation")
    # Modify data as you wish
    X = np.delete(X, len(X) - 1) if len(X) else np.array([])
    Y = np.delete(Y, len(Y) - 1) if len(Y) else np.array([])
    # Update canvas
    canvas.delete(tk.ALL)
    for x, y in zip(X, Y):
        canvas.create_rectangle(x,y,x+CELL_WIDTH,y+CELL_WIDTH)
    root.update()

canvas.bind("<Button-1>", one_generation)


root.mainloop()

#while True:
#    root.update()
#    time.sleep(1)
