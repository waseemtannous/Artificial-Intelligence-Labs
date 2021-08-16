class KnapsackProblem:  # a class that holds all relevant parameters for the knapsack problem
    def __init__(self, capacity, weights, profits, optimalSolution):
        self.capacity = capacity
        self.weights = weights
        self.profits = profits
        self.optimalSolution = optimalSolution

    def getCapacity(self):
        return self.capacity

    def getWeights(self):
        return self.weights

    def getProfits(self):
        return self.profits

    def getOptimalSolution(self):
        return self.optimalSolution
