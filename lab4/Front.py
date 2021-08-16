class Front:
    def __init__(self):
        self.members = []

    def crowdingDistanceSorting(self):
        self.members.sort()

    def addMembersToPopulation(self, population: list, size: int):  # adds members to population
        for i in range(size):
            population.append(self.members[i])

    def addMembersToFront(self, population: list):     # adds to members
        for member in population:
            if member.dominationCount == 0:
                self.members.append(member)
        for member in self.members:
            population.remove(member)
            for dominated in member.dominates:
                dominated.dominationCount -= 1
            member.dominates = []
