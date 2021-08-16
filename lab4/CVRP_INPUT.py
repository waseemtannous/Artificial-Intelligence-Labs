from math import sqrt

from lab4.City import City
from lab4.CVRP import CVRP
from lab4.Variables import TabuArgs


def getInput(probNum):
    file = open('INPUT\\' + str(probNum) + '.txt', 'r')  # input string
    for _ in range(3):
        file.readline()

    dimensionLine = file.readline()
    arr = [num for num in dimensionLine.split(' ')]
    dimension = int(arr[2]) # num of cities

    file.readline()

    capacityLine = file.readline()
    arr = [num for num in capacityLine.split(' ')]
    capacity = int(arr[2])

    file.readline()

    cityLine = file.readline()
    arr = [num for num in cityLine.split(' ')]
    depot = City(int(arr[0]) - 1, int(arr[1]), int(arr[2]), 0, 0, 0)

    cities = []
    for _ in range(dimension - 1):
        cityLine = file.readline()
        arr = [num for num in cityLine.split(' ')]
        city = City(int(arr[0]) - 1, int(arr[1]), int(arr[2]), 0, depot.x, depot.y)
        cities.append(city)

    file.readline()
    file.readline()

    for i in range(dimension - 1):
        demandLine = file.readline()
        arr = [num for num in demandLine.split(' ')]
        cities[i].value = int(arr[1])
        cities[i].capacity = int(arr[1])

    cities.insert(0, depot)

    distanceMat = calcDistanceMatrix(cities)
    cities.pop(0)

    problem = CVRP(cities, depot, distanceMat, capacity)

    return problem


def calcDistanceMatrix(cities):
    array = []
    numOfCities = len(cities)
    for i in range(numOfCities):
        arr = []
        for j in range(numOfCities):
            arr.append(distance(cities[i], cities[j]))
        array.append(arr)
    return array


def distance(city1, city2):
    x = city1.x - city2.x
    dx = x * x

    y = city1.y - city2.y
    dy = y * y

    return sqrt(dx + dy)


def getTabuArgs():
    file = open('ARGS\\TABU_ARGS.txt', 'r')  # input string

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxIter = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    localOptStop = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxTabu = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    numNeighbors = int(arr[2])

    return TabuArgs(maxIter, localOptStop, maxTabu, numNeighbors)
