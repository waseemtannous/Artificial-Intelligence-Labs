class CVRP:

    def __init__(self, distanceMatrix, depot, cities, capacity, size):
        self.distanceMatrix = distanceMatrix
        self.cities = cities
        self.depot = depot
        self.capacity = capacity
        self.size = size
        self.best = []
        self.bestFitness = 0

    def calcPathCost(self, path):
        totalCost = 0
        capacity = self.capacity
        index = 0
        totalCost += self.distanceMatrix[path[index]][0]
        capacity -= self.cities[path[index] - 1].capacity
        vehicles = 1

        while index < (len(path) - 1):
            city1 = path[index]
            city2 = path[index + 1]
            if self.cities[city2 - 1].capacity <= capacity:
                cost = self.distanceMatrix[city1][city2]
                capacity -= self.cities[city2 - 1].capacity
                totalCost += cost
            else:
                totalCost += self.distanceMatrix[city1][0]
                capacity = self.capacity
                vehicles += 1
                totalCost += self.distanceMatrix[city2][0]
                capacity -= self.cities[city2 - 1].capacity
            index += 1

        totalCost += self.distanceMatrix[path[index]][0]
        return totalCost, vehicles

    def pathToVehicles(self, path):
        capacity = self.capacity
        index = 0
        capacity -= self.cities[path[index] - 1].capacity

        pivot = 0
        subArrays = []

        while index < (len(path) - 1):
            city = path[index + 1]
            if self.cities[city - 1].capacity <= capacity:
                capacity -= self.cities[city - 1].capacity
            else:
                subArrays.append(path[pivot : index + 1])
                pivot = index + 1
                capacity = self.capacity
                capacity -= self.cities[city - 1].capacity
            index += 1

        subArrays.append(path[pivot : len(path)])

        for arr in subArrays:
            arr.insert(0, 0)
            arr.append(0)

        return subArrays

    def printSolution(self):
        print(self.bestFitness)
        paths = self.pathToVehicles(self.best)
        for path in paths:
            print(*path, sep=' ')
