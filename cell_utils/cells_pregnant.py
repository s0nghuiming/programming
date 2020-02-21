import tkinter as tk
import time
import numpy as np
from cell import Cell


# Static
CELL_SIZE = 4
CANVAS_SIZE = ( 80, 60 ) # in 10 * 10 grid
GRID_SIZE = 10
WINDOW_WIDTH = CANVAS_SIZE[0] * GRID_SIZE + CELL_SIZE
WINDOW_HEIGHT = CANVAS_SIZE[1] * GRID_SIZE + CELL_SIZE


# Data
MOST_LEFT = 0
MOST_RIGHT = WINDOW_WIDTH
MOST_TOP = 0
MOST_BOTTOM = WINDOW_HEIGHT
CELL_INIT_NUM = 10
SUM_CELL = CELL_INIT_NUM
LIMIT_NUM = 20


# Flags
PAUSE = False # False and True. Default is True.


# Cell chain init
cell_chain = {}
# Search map is for speeding search. each x coord as key of map. each y 
# with the same x consist a list after key x.
search_map = {}
X = np.random.randint( 0, CANVAS_SIZE[0], CELL_INIT_NUM ) * GRID_SIZE
Y = np.random.randint( 0, CANVAS_SIZE[1], CELL_INIT_NUM ) * GRID_SIZE
print(X)
print(Y)

# TK
root = tk.Tk()

# TK common items
label_sum = tk.Label(root, text="Total cell: ", font='fixed')
label_time = tk.Label(root, text=time.strftime('%H:%M:%S'), font='fixed' )
label_info = tk.Label(root, text='<location>', font='fixed' )

canvas = tk.Canvas(root, bg='white', width=800, height=600)
canvas.configure(bg='white')

canvas.pack(fill='y', side='right', expand=tk.YES)
label_time.pack(fill='x', side='top')
label_sum.pack(fill='x', side='top')
label_info.pack(fill='x', side='bottom')

# TK Other items
btn_pause = tk.Button(root, text="Pause", font='fixed')
btn_pause.pack(fill='none', expand='yes')

# Init cells
for x, y in zip(X, Y):
    rect_id = canvas.create_rectangle(x,y,x+CELL_SIZE,y+CELL_SIZE)
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

# Common function

# time_update
#   update text of time label
def time_update():
    root.after(1000, time_update)
    curtime = time.strftime('%H:%M:%S')
    label_time.config(text=curtime)


# Function

#
def create_cell(cell = None):
    if cell:
        rect_id = canvas.create_rectangle(cell.x,
                          cell.y,
                          cell.x+CELL_SIZE,
                          cell.y+CELL_SIZE )
        cell.serialno = rect_id
        cell_chain[rect_id] = cell
        SUM_CELL = SUM_CELL + 1

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
                        new_cells.append( (xs + dx, ys + dy ) )
        return new_cells
    else:
        return None

def one_generation():
    global SUM_CELL
    global PAUSE
    loop_id = None
    loop_id = root.after(500, one_generation)

    if True == PAUSE:
        if loop_id:
            root.after_cancel(loop_id)
        root.update()
    else:
        # Modify data as you wish
        if len(cell_chain) < LIMIT_NUM:
            father_id = np.random.choice(list(cell_chain))
            spawn_cells = spawn(cell_chain[father_id])
            #canvas.delete(tk.ALL)
            for x, y in spawn_cells:
                s_c = Cell(x, y)
                rect_id = canvas.create_rectangle(s_c.x,
                                              s_c.y,
                                              s_c.x+CELL_SIZE,
                                              s_c.y+CELL_SIZE )
                s_c.serialno = rect_id
                cell_chain[rect_id] = s_c
                SUM_CELL = SUM_CELL + 1
            if 0 != len(spawn_cells):
                pass
            label_sum.config(text="Total cell: " + str(len(cell_chain)))
        else:
            print("Maximum exceeds.")
            root.after_cancel(loop_id)
            print("# ----- Cells ----- \n")
            for k, c in cell_chain.items():
                print("{0} {1} {2}".format(str(k), str(c.x), str(c.y)))
            print("\n# ----------\n")

        root.update()

# Pause not impl
def set_pause(event):
    global PAUSE
    if False == PAUSE:
        PAUSE = True
        btn_pause.config(text='Resume')
        print("Paused")
    else:
        PAUSE = False
        btn_pause.config(text='Pause')
        root.after(0, one_generation)
        print("Resumed")

btn_pause.bind("<Button-1>", set_pause)

# Label info
def update_info(event):
    label_info.config(text=f"x:{event.x},y:{event.y}")

canvas.bind('<Motion>', update_info)

# Collect cell
def collect_cell(event):
    x = event.x // GRID_SIZE * GRID_SIZE
    y = event.y // GRID_SIZE * GRID_SIZE
    print(f"x:{x}, y:{y}")

canvas.bind('<Button-1>', collect_cell)


root.after(0, one_generation)
root.after(0, time_update)
root.mainloop()

#while True:
#    root.update()
#    time.sleep(1)
