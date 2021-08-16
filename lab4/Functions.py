from random import randint


def initGreedySol(cities, distanceMatrix):  # TSP: nearest neighbor heuristic
    allCities = [city.name for city in cities]
    array = []
    city = allCities[randint(0, len(allCities) - 1)]
    city = 0
    # array.append(city)
    # dictionary = {city: True}
    dictionary = {}
    index = len(allCities)
    # index -= 1
    while index > 0:
        distanceArray = distanceMatrix[city]
        minCity = 1
        minDistance = float('inf')
        for currentCity in allCities:
            distance = distanceArray[currentCity]
            if 0 < distance < minDistance and not dictionary.get(currentCity, False):
                minDistance = distance
                minCity = currentCity
        array.append(minCity)
        dictionary[minCity] = True
        city = minCity
        index -= 1
    return array


def GAGreedySol(size, problem):   # TSP: nearest neighbor heuristic
    array = []
    city = randint(1, size)
    array.append(city)
    dictionary = {city: True}
    index = size
    index -= 1
    while index > 0:
        distanceArray = problem.distancMat[city]
        minCity = 1
        minDistance = float('inf')
        for i in range(1, len(distanceArray)):
            distance = distanceArray[i]
            if 0 < distance < minDistance and not dictionary.get(i, False):
                minDistance = distance
                minCity = i
        array.append(minCity)
        dictionary[minCity] = True
        city = minCity
        index -= 1
    return array


def getNeighborhood(bestCandidate, numNeighbors):
    return [mutate(bestCandidate) for _ in range(numNeighbors)]


def mutate(bestCandidate):
    return simpleInversionMutation(bestCandidate)


def simpleInversionMutation(sol):
    string = sol[:]
    i1 = randint(0, len(sol) - 1)
    i2 = randint(0, len(sol) - 1)
    if i1 > i2:
        i1, i2 = i2, i1
    while i1 < i2:
        string[i1], string[i2] = string[i2], string[i1]
        i1 += 1
        i2 -= 1
    return string


def calcPathCost(cities, distanceMatrix):
    cost = distanceMatrix[cities[0]][0]

    for i in range(len(cities) - 1):
        city1 = cities[i]
        city2 = cities[i + 1]
        cost += distanceMatrix[city1][city2]

    cost += distanceMatrix[cities[-1]][0]
    return cost
