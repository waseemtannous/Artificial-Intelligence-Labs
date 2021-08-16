from lab4.Object import Object


class Sack:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.value = 0
        self.objects: list = []

    def addObject(self, object: Object):
        self.objects.append(object)

    def sumDensities(self, sumDensities: dict):
        for object in self.objects:
            if not sumDensities.get(object, False):
                sumDensities[object] = object.density
            else:
                sumDensities[object] += object.density

    def calculateWeight(self, vector: list):
        weight = 0
        for i in range(len(vector)):
            if vector[i] == 0:
                continue
            weight += self.objects[i].weight
        return weight

    def calculateValue(self, vector: list):
        value = 0
        for i in range(len(vector)):
            if vector[i] == 0:
                continue
            value += self.objects[i].value
        return value


