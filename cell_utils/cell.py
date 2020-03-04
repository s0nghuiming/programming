#


# CELL chain
class Cell():
    def __init__(self, x, y, serialno = -1):
        self.serialno = serialno
        self.x = x
        self.y = y
        self.father = None

class Cell_Chain(dict):
    def __init__(self):
        super(Cell_Chain, self).__init__()
