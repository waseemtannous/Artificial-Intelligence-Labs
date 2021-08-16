from random import randint


class GAstruct:
    def __init__(self, string, fitness, AGE_MIN, AGE_MAX):
        self.string = string
        self.fitness = fitness
        self.age = randint(AGE_MIN, AGE_MAX)
        self.AGE_MIN = AGE_MIN
        self.AGE_MAX = AGE_MAX
        self.dominates = []
        self.dominationCount = 0
        self.pathCost = 0
        self.numberOfVehicles = 0

    def getString(self):
        return self.string

    def getFitness(self):
        return self.fitness

    def setString(self, string):
        self.string = string

    def setFitness(self, fitness):
        self.fitness = fitness

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = age

    def updateAge(self):
        self.age += 1

    def zeroAge(self):
        self.age = 0

    def __gt__(self, other):
        return self.getFitness() >= other.getFitness()

    def __lt__(self, other):
        return self.getFitness() < other.getFitness()
