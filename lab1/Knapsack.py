from lab1.GAstruct import GAstruct
from random import random
from copy import deepcopy
from lab1.Functions import *


class Knapsack:

    def __init__(self, knapsackProblem, args):
        self.args = args
        self.crossoverType = args.CROSS
        self.selectionType = args.SELECTION
        self.capacity = knapsackProblem.getCapacity()
        self.optimalSolution = knapsackProblem.getOptimalSolution()
        self.weights = knapsackProblem.getWeights()
        self.profits = knapsackProblem.getProfits()
        self.maxProfit = sum(knapsackProblem.getProfits())
        self.tsize = len(knapsackProblem.getOptimalSolution())
        self.esize = int(self.args.GA_ELITRATE * self.args.GA_POPSIZE)
        self.population = []
        self.nextPopulation = []
        self.susPopulation = []
        self.susInitArray = True
        self.susIndex = 0

    def initPopulation(self):
        for _ in range(self.args.GA_POPSIZE):
            randomStr1 = []
            randomStr2 = []
            for _ in range(self.tsize):
                randomStr1.append(randint(0, 1))
                randomStr2.append(randint(0, 1))
            member1 = GAstruct(randomStr1, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member2 = GAstruct(randomStr2, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            self.population.append(member1)
            self.nextPopulation.append(member2)

    def calcStringFitness(self, string1, string2):
        if self.priceFitness(string1) < self.priceFitness(string2):
            return string1
        else:
            return string2

    def calcFitness(self):
        for person in self.population:
            fitness = self.priceFitness(person.getString())
            person.setFitness(fitness)

    def priceFitness(self, string):
        price = 0
        weight = 0
        for j in range(self.tsize):
            price += self.profits[j] * string[j]
            weight += self.weights[j] * string[j]

        if weight > self.capacity:
            price = 0

        return abs(self.maxProfit - price)

    def mutate(self, member):
        ipos = randint(0, self.tsize - 1)
        string = member.getString()
        if string[ipos] == 0:
            string[ipos] = 1
        else:
            string[ipos] = 0
        member.setString(string)

    def mate(self):
        elitism(self)

        if self.crossoverType == CrossoverType.ONE_POINT:
            self.onePointCrossover()
        elif self.crossoverType == CrossoverType.TWO_POINT:
            self.twoPointCrossover()
        else:
            self.uniformCrossover()

    def onePointCrossover(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            person1, person2 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)
            spos = randint(0, self.tsize - 1)

            str1 = deepcopy(person1.getString())
            str2 = deepcopy(person2.getString())

            string1 = []
            string2 = []

            for j in range(spos):
                string1.append(str1[j])
                string2.append(str2[j])

            for j in range(spos, self.tsize):
                string1.append(str2[j])
                string2.append(str1[j])

            string = self.calcStringFitness(string1, string2)
            member = GAstruct(string, self.priceFitness(string), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def twoPointCrossover(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            spos1 = randint(0, self.tsize - 2)
            spos2 = randint(spos1 + 1, self.tsize - 1)

            person1, person2 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)

            str1 = deepcopy(person1.getString())
            str2 = deepcopy(person2.getString())

            string1 = []
            string2 = []

            for j in range(spos1):
                string1.append(str1[j])
                string2.append(str2[j])

            for j in range(spos1, spos2):
                string1.append(str2[j])
                string2.append(str1[j])

            for i in range(spos2, self.tsize):
                string1.append(str1[i])
                string2.append(str2[i])

            string = self.calcStringFitness(string1, string2)
            member = GAstruct(string, self.priceFitness(string), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def uniformCrossover(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            person1, person2 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)

            str1 = deepcopy(person1.getString())
            str2 = deepcopy(person2.getString())

            string1 = []
            string2 = []

            for j in range(0, self.tsize):
                if (int(random.random()) % 2) == 0:
                    string1.append(str1[j])
                    string2.append(str2[j])
                else:
                    string1.append(str2[j])
                    string2.append(str1[j])

            string = self.calcStringFitness(string1, string2)
            member = GAstruct(string, self.priceFitness(string), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)
