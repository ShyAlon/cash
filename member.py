import numpy as np

class Member:
     def __init__(self):
         self.quality = 0
         self.map = None
         self.features = []
         self.x = []
         self.y = []
         self.recommendations = []

     def set_x(self, source):
          del self.x[:]
          for i in source:
               self.x.append(i)
     def set_y(self, source):
          del self.y[:]
          for i in source:
               self.y.append(i)