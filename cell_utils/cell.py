from collections.abc import MutableMapping
#


# CELL chain
class Cell():
    def __init__(self, x, y, point=[], serialno = -1):
        self.serialno = serialno
        self.x = x
        self.y = y
        self.point = [x, y]
        self.father = None

""" Cell Chain

"""
class Cell_Chain(MutableMapping):
    def __init__(self, data=()):
        self.__cells = {}
        self.__searchmap = {}
        self.__outlinemap = {}
        self.update(data)

    """__cells is default data for manipulation."""
    def __getitem__(self, key):
        return self.__cells[key]

    def __delitem__(self, key):
        value = self[key]
        del self.__cells[key]

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        self.__cells[key] = value

    def __iter__(self):
        return iter(self.__cells)

    def __len__(self):
        return len(self.__cells)

    def __repr__(self):
        return f"{type(self).__name__}({self.__cells})"

    def prt_cell(self):
        return f"{self.__cells}"

    def prt_searchmap(self):
        return f"{self.__searchmap}"

    def prt_outlinemap(self):
        return f"{self.__outlinemap}"

    def contains(self, point=[]):
        x = point[0]
        y = point[1]
        if x in self.__searchmap and y in self.__searchmap[x]:
            return True
        else:
            return False

    def add_to_search_map(self, point=None):
        x = point[0]
        y = point[1]
        if x in self.__searchmap:
            if not y in self.__searchmap[x]:
                self.__searchmap[x].append(y)
            else:
                pass # x, y already in map.
        else:
            self.__searchmap[x] = []
            self.__searchmap[x].append(y)

    def get_search_map(self):
        return self.__searchmap

