import tkinter as tk
import time
import numpy as np
from cell import Cell


# Static
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_WIDTH = 4
LIMIT_NUM = 500


# Data
MOST_LEFT = CELL_WIDTH / 2
MOST_RIGHT = WINDOW_WIDTH - CELL_WIDTH / 2
MOST_TOP = CELL_WIDTH / 2
MOST_BOTTOM = WINDOW_HEIGHT - CELL_WIDTH / 2
CELL_INIT_NUM = 10
SUM_CELL = CELL_INIT_NUM


# Flags
PAUSE = False


# Cell chain init
cell_chain = {}
# Search map is for speeding search. each x coord as key of map. each y 
# with the same x consist a list after key x.
search_map = {}
X = np.random.randint( MOST_LEFT, MOST_RIGHT - CELL_WIDTH, CELL_INIT_NUM )
Y = np.random.randint( MOST_TOP, MOST_BOTTOM - CELL_WIDTH, CELL_INIT_NUM )


# TK
root = tk.Tk()

# TK common items
label_sum = tk.Label(root, text="Total cell: ")
label_time = tk.Label(root, text=time.strftime('%H:%M:%S'), )

canvas = tk.Canvas(root, bg='white', width=800, height=600)
canvas.configure(bg='white')

canvas.pack(fill='y', side='right', expand=tk.YES)
label_time.pack(fill='x', side='top')
label_sum.pack(fill='x', side='top')

# TK Other items
btn_pause = tk.Button(root, text="Pause")
btn_pause.pack(fill='none', expand='yes')

# Init cells
for x, y in zip(X, Y):
    rect_id = canvas.create_rectangle(x,y,x+CELL_WIDTH,y+CELL_WIDTH)
    cell = Cell(x, y, serialno=rect_id)
    cell_chain[rect_id] = cell
    # mapping with x , y
    if x in search_map:
        if not y in search_map[x]:
            search_map[x].append(y)
        else:
            pass # x, y already in map.
    else:
        search_map[x] = []
        search_map[x].append(y)

# Function

# time_update
#   update text of time label
def time_update():
    root.after(1000, time_update)
    curtime = time.strftime('%H:%M:%S')
    label_time.config(text=curtime)

# spawn:
#    One alive cell spawns his son.
#    cell: alive cell,
#    speed: how many sons born in one spawn,
def spawn(cell=None, speed=1):
    if None != cell:
        xs = cell.x
        ys = cell.y
        new_cells = []
        delta_map = [
                      (-10,  0 ), 
                      (-10,  10), 
                      (-10, -10), 
                      (  0,  10), 
                      (  0, -10), 
                      ( 10,   0),
                      ( 10,  10),
                      ( 10, -10),
                  ]
        for i in range(0,speed):
            dx, dy = delta_map[np.random.randint(len(delta_map))]
            if xs + dx < MOST_RIGHT or xs + dx > MOST_LEFT:
                if ys + dy < MOST_BOTTOM or ys + dy > MOST_TOP:
                    if not (xs + dx) in search_map or not (ys + dy) in search_map[xs+dx]:
                        new_cells.append( Cell(xs + dx, ys + dy ) )
        return new_cells
    else:
        return None

def one_generation():
    global SUM_CELL
    loop_id = None
    loop_id = root.after(500, one_generation)
    # Modify data as you wish
    if len(cell_chain) < LIMIT_NUM:
        father_id = np.random.choice(list(cell_chain))
        spawn_cells = spawn(cell_chain[father_id])
        #canvas.delete(tk.ALL)
        for s_c in spawn_cells:
            rect_id = canvas.create_rectangle(s_c.x, 
                                          s_c.y, 
                                          s_c.x+CELL_WIDTH, 
                                          s_c.y+CELL_WIDTH)
            s_c.serialno = rect_id
            cell_chain[rect_id] = s_c
            SUM_CELL = SUM_CELL + 1
        if 0 != len(spawn_cells):
            pass
        label_sum.config(text="Total cell: " + str(len(cell_chain)))
    else:
        print("Maximum exceeds.")
        root.after_cancel(loop_id)

    root.update()

# Pause not impl
def set_pause(event):
    print("Paused")

btn_pause.bind("<Button-1>", set_pause)


root.after(0, one_generation)
root.after(0, time_update)
root.mainloop()

#while True:
#    root.update()
#    time.sleep(1)
