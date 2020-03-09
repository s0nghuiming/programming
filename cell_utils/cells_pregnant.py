import tkinter as tk
import time
import numpy as np
from cell import Cell, Cell_Chain


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
LIMIT_NUM = 1200


# Flags
PAUSE = False # Pause the progress. Default is False.


# Cell chain init
cell_chain = Cell_Chain()
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
    # here init points dont overlap, so write to search map directly.
    # mapping with x , y
    if not cell_chain.contains([x, y]):
        cell_chain.add_to_search_map([ x, y ], tk_id=rect_id)

# Common function

# time_update
#   update text of time label
def time_update():
    root.after(1000, time_update)
    curtime = time.strftime('%H:%M:%S')
    label_time.config(text=curtime)


# Function

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
        return rect_id
    else:
        return None

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
        free_direction = 8 # default for free space around a cell
        for i in range(0,speed):
            direction = np.random.randint(len(delta_map))
            for i in range(0, 8)
            dx, dy = delta_map[direction]
            
            if xs + dx < MOST_RIGHT and xs + dx > MOST_LEFT:
                if ys + dy < MOST_BOTTOM and ys + dy > MOST_TOP:
                    if not cell_chain.contains([(xs + dx), (ys + dy)]):
                        new_cells.append( (xs + dx, ys + dy ) )
                    else:
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
            outline_image = cell_chain.get_outline(mode='')
            print(cell_chain.prt_searchmap())
            print(outline_image)
            index = np.random.choice(range(len(outline_image)))
            print(index)
            print(outline_image[index])
            father_id = cell_chain.get_search_map(
                                            point = outline_image[index],
                                            mode='single')
            spawn_cells = spawn(cell_chain[father_id])
            for x, y in spawn_cells:
                # mapping with x , y
                if cell_chain.contains([x, y]):
                    print("hit")
                else:
                    rect_id = create_cell(x, y, father=father_id)
                    cell_chain.add_to_search_map([x, y], tk_id=rect_id)

            if 0 != len(spawn_cells):
                pass
            label_sum.config(text="Total cell: " + str(len(cell_chain)))
        else:
            print("Maximum exceeds.")
            root.after_cancel(loop_id)
            print("# ----- Cells ----- \n")
            print(cell_chain.prt_image())
            #for k, c in cell_chain.items():
            #    print("{0} {1} {2} {3}".format(str(k), str(c.father), str(c.x), str(c.y)))
            #print("\n# ----------\n")
            #sum = 0
            #for a in cell_chain.get_search_map():
            #    sum = sum + len(cell_chain.get_search_map()[a])
            #    print(str(a) + ":" + str(len(cell_chain.get_search_map()[a])))
            #print("Sum: " + str(sum))
            #for cell in cell_chain.values():
            #    if cell_chain.contains([cell.x, cell.y]):
            #        pass
            #    else:
            #        print(cell.x, ' ', cell.y)

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
    if cell_chain.contains([x, y]):
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
