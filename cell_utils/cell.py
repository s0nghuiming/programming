from collections.abc import MutableMapping
#


# CELL chain
class Cell():
    def __init__(self, x, y, serialno = -1):
        self.serialno = serialno
        self.x = x
        self.y = y
        self.father = None

class Cell_Chain(MutableMapping):
    def __init__(self, data=()):
        self.__cells = {}
        self.update(data)

    def __getitem__(self, key):
        return self.__cells[key]

    def __delitem__(self, key):
        value = self[key]
        del self.__cells[key]
        self.pop(value, None)

    def __setitem__(self, key, value):
        if key in self:
            del self[self[key]]
        if value in self:
            del self[value]
        self.__cells[key] = value
        self.__cells[value] = key

    def __iter__(self):
        return iter(self.__cells)

    def __len__(self):
        return len(self.__cells)

    def __repr__(self):
        return f"{type(self).__name__}({self.__cells})"

