from math import sqrt


class City:
    def __init__(self,name,X,Y,value,depotX, depotY):
        self.name = name
        self.x = X
        self.y = Y
        self.distancFromDepot = self.calculateDistance(depotX, depotY)
        self.value = value
        self.capacity = value

    def calculateDistance(self, x, y):
        deltaX = (self.x - x) ** 2
        deltaY = (self.y - y) ** 2
        return sqrt(deltaY + deltaX)