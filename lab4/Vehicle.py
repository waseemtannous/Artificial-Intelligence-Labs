class Vehicle:
    def __init__(self, capacity, depot):
        self.capacity = capacity
        self.depot = depot
        self.cities = []
        self.centerX = 0
        self.centerY = 0
        self.currValue = capacity
        self.bestPath = []
        self.bestPathCost = 0

    def getNearestCity(self, cities):
        NeaerestCity, minDistance = None, float('inf')
        for city in cities:
            distanc = city.calculateDistance(self.centerX, self.centerY)
            if (distanc < minDistance):
                NeaerestCity = city
                minDistance = distanc
        return NeaerestCity

    def addCity(self, cities):
        if len(self.cities) == 0:
            nearestCity = self.getFarCity(cities)
        else:
            nearestCity = self.getNearestCity(cities)
        if nearestCity is None:
            return False
        valueOfCity = nearestCity.value
        if self.currValue >= valueOfCity:
            cities.remove(nearestCity)
            self.currValue -= valueOfCity
            self.cities.append(nearestCity)
            return True
        return False

    def addCities(self, cities):
        flag = True
        while self.currValue > 0 and flag:
            flag = self.addCity(cities)
            self.updateCenter()

    def getFarCity(self, cities):
        farCity, maxDistance = 0, 0
        for city in cities:
            if city.distancFromDepot > maxDistance:
                farCity = city
                maxDistance = city.distancFromDepot
        return farCity

    def updateCenter(self):
        city = self.cities[-1]
        x = city.x
        y = city.y
        self.centerX = float(((self.centerX * (len(self.cities) - 1)) + x) / len(self.cities))
        self.centerY = float(((self.centerY * (len(self.cities) - 1)) + y) / len(self.cities))

    def printPath(self):
        print(self.depot.name, ' ', end='')
        for city in self.cities:
            print(city.name, ' ', end='')
        print(self.depot.name)
