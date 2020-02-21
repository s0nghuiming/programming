#


# CELL chain
class Cell():
    def __init__(self, x, y, serialno = -1):
        self.serialno = serialno
        self.x = x
        self.y = y
        self.father = None

