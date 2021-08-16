class City:

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.capacity = 0

    def setDemand(self, demand):
        self.capacity = demand

    def __lt__(self, other):
        return self.capacity < other.demand

    def __gt__(self, other):
        return self.capacity > other.demand
