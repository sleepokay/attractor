import numpy

class Attractor():
    def __init__(self):
        self.points = []
        self.xmin = float("inf")
        self.ymin = float("inf")
        self.xmax = float("-inf")
        self.ymax = float("-inf")

    def update_bounds(self, x, y):
        self.xmin = min(self.xmin, x)
        self.ymin = min(self.ymin, y)
        self.xmax = max(self.xmax, x)
        self.ymax = max(self.ymax, y)