from collections.abc import MutableMapping
import numpy as np
from scipy.ndimage.interpolation import shift
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
    def __init__(self, shape=(81, 61), data=()):
        self.__cells = {}
        # Search map
        # Search map is for speeding search. each x coord as key of map. each
        # y with the same x consist a list after key x.
        self.__searchmap = {}
        self.__shape = shape
        self.__image = np.zeros(shape, dtype = 'uint8')
        self.update(data)

    """__cells is default data for manipulation."""
    def __getitem__(self, key):
        return self.__cells[key]

    def __delitem__(self, key):
        value = self[key]
        del self.__cells[key]
        self.__searchmap[value.x].remove([value.y])
        if 0 == len(self.__searchmap[value.x]):
            del self.__searchmap[value.x]
        self.__image[value.x//10][value.y//10] = np.uint(0)

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        self.__cells[key] = value
        self.__image[value.x//10][value.y//10] = np.uint(255)

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

    def prt_image(self):
        import cv2
        #cv2.imwrite("outline.png", self.__image)
        return f"{self.__image}"

    def contains(self, point=[]):
        x = point[0]
        y = point[1]
        if x in self.__searchmap and y in self.__searchmap[x]:
            return True
        else:
            return False

    def add_to_search_map(self, point=None, tk_id=0):
        x = point[0]
        y = point[1]
        if x in self.__searchmap:
            if not y in self.__searchmap[x]:
                self.__searchmap[x][y] = tk_id
            else:
                pass # x, y already in map.
        else:
            self.__searchmap[x] = {}
            self.__searchmap[x][y] = tk_id

    """
    point: tuple of axis.
    mode:  'all' is for all print. 'single' for one print.

    """
    def get_search_map(self, point=None, mode='all'):
        if 'all' != mode:
            return self.__searchmap[point[0]][point[1]]
        else:
            return self.__searchmap

    def get_outline(self, mode='all'):
        rev = -1-self.__image # this change 0 to 255, 255 to 0 for a uint8 matrix
        map1 = shift(rev,  1, cval=np.NaN) - rev
        map2 = shift(rev, -1, cval=np.NaN) - rev

        outline = np.array(
                [ [ 0 if j <= 127 else 255 for j in i ] for i in map1 + map2 ],
                dtype='uint8' # 0: black, 255: white
                ) 
        outline_index = np.where(outline == np.uint(255))
        index = list(zip(outline_index[0] * 10, outline_index[1] * 10))

        if 'all' == mode:
            return outline
        else:
            return index

