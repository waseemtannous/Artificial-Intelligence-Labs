from random import uniform


class Particle:
    def __init__(self, string, fitness, velocityVector):
        self.string = string
        self.bestString = string
        self.fitness = fitness
        self.bestFitness = fitness
        self.velocityVector = velocityVector

    def getString(self):
        return self.string

    def getBestString(self):
        return self.bestString

    def getFitness(self):
        return self.fitness

    def getBestFitness(self):
        return self.bestFitness

    def setString(self, string):
        self.string = string

    def setBestString(self, bestString):
        self.bestString = bestString

    def setFitness(self, fitness):
        self.fitness = fitness

    def setBestFitness(self, bestFitness):
        self.bestFitness = bestFitness

    def update(self, Gbest, C1, C2, W):
        r1 = uniform(0, 1)
        r2 = uniform(0, 1)

        new_string1 = self.newString(self.getBestString(), self.getString(), r1 * C1)
        new_string2 = self.newString(Gbest, self.getString(), r2 * C2)
        add_String = self.addString(new_string2, new_string1)
        self.velocityVector = [(self.velocityVector[i] * W) for i in range(len(self.velocityVector))]

        self.velocityVector = self.addString(self.velocityVector, add_String)
        self.string = self.addString(self.string, self.velocityVector)

        self.string = [round(self.string[i]) for i in range(len(self.string))]
        self.velocityVector = [round(self.velocityVector[i]) for i in range(len(self.velocityVector))]

    def addString(self, str1, str2):
        new_string = []
        for i in range(len(str1)):
            new_string.append((str1[i]) + (str2[i]))
        return new_string

    def newString(self, str1, str2, x):
        new_string = []
        for i in range(len(str1)):
            new_string.append((x * ((str1[i]) - (str2[i]))))
        return new_string

    def __gt__(self, other):
        return self.getFitness() >= other.getFitness()

    def __lt__(self, other):
        return self.getFitness() < other.getFitness()