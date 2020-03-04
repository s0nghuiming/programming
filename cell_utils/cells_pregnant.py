import tkinter as tk
import time
import numpy as np
from cell import Cell
from scipy.ndimage.interpolation import shift


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
LIMIT_NUM = 1000


# Flags
PAUSE = False # Pause the progress. Default is False.


# Cell chain init
cell_chain = {}
# Search map
# Search map is for speeding search. each x coord as key of map. each y 
# with the same x consist a list after key x.
search_map = {}
# Outline map
# Outline is the outline of the integrate of all cells that closed to 
# each other. It is used to store the coordinates of the cells on the 
# outline.
outline_map = np.zeros(CANVAS_SIZE, dtype='uint8')

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
    # outline
    outline_map[x//10][y//10] = 255
    # here init points dont overlap, so write to search map directly.
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

# get outline:
# this function is to find outline of a mass of cells.
# Input: outline_map
# Output: a numpy array. if value is 255, it is the outline of the mass.
def get_outline():
    global outline_map
    rev = -1-outline_map # this change 0 to 255, 255 to 0 for a uint8 matrix
    map1 = shift(rev, 1, cval=np.NaN) - rev
    map2 = shift(rev, -1, cval=np.NaN) - rev

    outline = np.array(
            [ [ 0 if j <= 127 else 255 for j in i ] for i in map1 + map2 ],
            dtype='uint8'
            )

    return outline

# create a cell
def create_cell(x, y, father=None):
    global SUM_CELL
    if x and y:
        cell = Cell(x, y)
        cell.father = father
        rect_id = canvas.create_rectangle(cell.x,
                          cell.y,
                          cell.x+CELL_SIZE,
                          cell.y+CELL_SIZE )
        cell.serialno = rect_id
        cell_chain[rect_id] = cell
        SUM_CELL = SUM_CELL + 1
        outline_map[x//10][y//10] = 255

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
                      (-10,   0), 
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
            if xs + dx < MOST_RIGHT and xs + dx > MOST_LEFT:
                if ys + dy < MOST_BOTTOM and ys + dy > MOST_TOP:
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
                # mapping with x , y
                if x in search_map and y in search_map[x]:
                    print("hit")
                else:
                    create_cell(x, y, father=father_id)

                    if x in search_map:
                        #if not y in search_map[x]:
                        search_map[x].append(y)
                    else:
                        search_map[x] = []
                        search_map[x].append(y)

            if 0 != len(spawn_cells):
                pass
            label_sum.config(text="Total cell: " + str(len(cell_chain)))
        else:
            print("Maximum exceeds.")
            root.after_cancel(loop_id)
            print("# ----- Cells ----- \n")
            for k, c in cell_chain.items():
                print("{0} {1} {2} {3}".format(str(k), str(c.father), str(c.x), str(c.y)))
            print("\n# ----------\n")

        root.update()

# Pause the progress
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

# Mouse position info
def update_info(event):
    label_info.config(text=f"x:{event.x},y:{event.y}")

canvas.bind('<Motion>', update_info)

# Collect cell
collect_num = 0
def collect_cell(event):
    global collect_num
    x = event.x // GRID_SIZE * GRID_SIZE
    y = event.y // GRID_SIZE * GRID_SIZE
    # If (x,y) is the cell exists in cell_chain/search_map
    if x in search_map and y in search_map[x]:
        collect_num = collect_num + 1
        print(f"#{collect_num:3d}: x:{x}, y:{y}")

def clear_collection(event):
    global collect_num
    collect_num = 0

canvas.bind('<Button-1>', collect_cell)
canvas.bind('<Button-3>', clear_collection)


# TK loops
root.after(0, one_generation)
root.after(0, time_update)
root.mainloop()
