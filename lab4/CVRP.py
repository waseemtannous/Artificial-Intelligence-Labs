from lab4.TabuSearch import *


class CVRP:
    def __init__(self, cities, depot, distancMat, capacity):
        self.cities = cities
        self.depot = depot
        self.distancMat = distancMat
        self.vehicles = []
        self.capacity = capacity
        self.cost = 0

    def divideVehicles(self):
        while len(self.cities) > 0:
            vehicle = Vehicle(self.capacity, self.depot)
            self.vehicles.append(vehicle)
            vehicle.addCities(self.cities)
        for vehicle in self.vehicles:
            vehicle.printPath()

    def solveTsp(self, args):
        for vehicle in self.vehicles:
            tabuSearch(args, vehicle, self.distancMat, len(self.vehicles))

        for vehicle in self.vehicles:
            print(vehicle.bestPath, ', cost: ', vehicle.bestPathCost)
            self.cost += vehicle.bestPathCost
        print('Total Cost: ', self.cost)

    def calcPathCost(self, path):
        totalCost = 0
        capacity = self.capacity
        index = 0
        totalCost += self.distancMat[path[index]][0]
        capacity -= self.cities[path[index] - 1].capacity
        vehicles = 1

        while index < (len(path) - 1):
            city1 = path[index]
            city2 = path[index + 1]
            if self.cities[city2 - 1].capacity <= capacity:
                cost = self.distancMat[city1][city2]
                capacity -= self.cities[city2 - 1].capacity
                totalCost += cost
            else:
                totalCost += self.distancMat[city1][0]
                capacity = self.capacity
                vehicles += 1
                totalCost += self.distancMat[city2][0]
                capacity -= self.cities[city2 - 1].capacity
            index += 1

        totalCost += self.distancMat[path[index]][0]
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
                subArrays.append(path[pivot: index + 1])
                pivot = index + 1
                capacity = self.capacity
                capacity -= self.cities[city - 1].capacity
            index += 1

        subArrays.append(path[pivot: len(path)])

        for arr in subArrays:
            arr.insert(0, 0)
            arr.append(0)

        return subArrays

    def printSolution(self, best):
        print(best.pathCost)
        paths = self.pathToVehicles(best.string)
        for path in paths:
            print(*path, sep=' ')

