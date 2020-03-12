import tkinter as tk
import time
import numpy as np
from cell import Cell


# Static
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_WIDTH = 4


# Data
MOST_LEFT = CELL_WIDTH / 2
MOST_RIGHT = WINDOW_WIDTH - CELL_WIDTH / 2
MOST_TOP = CELL_WIDTH / 2
MOST_BOTTOM = WINDOW_HEIGHT - CELL_WIDTH / 2
CELL_INIT_NUM = 10
SUM_CELL = CELL_INIT_NUM
LIMIT_NUM = 100


# Flags
PAUSE = False # False and True. Default is True.


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

# Common function

# time_update
#   update text of time label
def time_update():
    root.after(1000, time_update)
    curtime = time.strftime('%H:%M:%S')
    label_time.config(text=curtime)


# Function

# spawn:
#    One alive cell spawns his son.
#    cell: alive cell,
#    speed: how many sons born in one spawn,
#    Description: || 占位符
#    |生育新细胞的条件比较苛刻。最好是不要生在其他细胞上，也就是不重合；
#    |按照|delta_map||的定义，是一个|3*3|的矩阵的中心为父亲细胞，外围八个
#    |点作为子细胞。按这个方法简化的话，所有的细胞都应该出现在等距离的点
#    |阵中。所以，要把细胞初始化的代码做修改，改为在矩阵的点上生成初始点。
#    |另外，在本函数中，目前的判断条件是子细胞不能超出边框，而且新子细胞
#    |不能和已有细胞重合。如果不满足条件，则返回空。这样的话此次函数调用
#    |就不产生新细胞，需要等待下一轮调用，而如果下一轮也如此轮空的话，那么
#    |很不幸，需要等更多的时间了。这种情况发生的概率将随着细胞的数量变大而
#    |变大。如何能解决这种时间的浪费呢？
#    |引入卷积，将能解决这个问题。接下来介绍……
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


root.after(0, one_generation)
root.after(0, time_update)
root.mainloop()

#while True:
#    root.update()
#    time.sleep(1)

https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds
https://pillow.readthedocs.io/en/stable/handbook/tutorial.html
https://docs.scipy.org/doc/numpy/reference/
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html
https://gist.github.com/kashefy/00279f9edb3a56fd3d15
https://pypi.org/project/Pillow/#files
# python inherit dict
https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/
http://www.kr41.net/2016/03-23-dont_inherit_python_builtin_dict_type.html
# Download files via us server
ssh guest@143.183.30.151 # guest_123!
