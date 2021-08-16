class MultiKnapsackProblem:
    def __init__(self, sacks: list, optimum: int, values: list, sumDensities: dict, size: int, fitness):
        self.sacks = sacks
        self.sumDensities = sumDensities
        self.optimum = optimum
        self.values = values
        self.sumValues = sum(values)
        self.size = size
        self.bestValue = 0
        self.bestVector = []
        self.deadEnd: dict = {'': False}
        self.fitness = fitness

    def getSacksWeights(self) -> list:
        return [sack.weight for sack in self.sacks]
