from lab1.Functions import *
from lab1.GAstruct import GAstruct
from random import randint, random


class GeneticAlgorithm:

    def __init__(self, args):
        self.args = args
        self.crossoverType = args.CROSS
        self.fitnessType = args.FITNESS
        self.selectionType = args.SELECTION
        self.tsize = len(self.args.GA_TARGET)
        self.esize = int(self.args.GA_ELITRATE * self.args.GA_POPSIZE)
        self.population = []
        self.nextPopulation = []
        self.susPopulation = []
        self.susInitArray = True
        self.susIndex = 0

    def initPopulation(self):
        for _ in range(self.args.GA_POPSIZE):
            randomStr1 = ''
            randomStr2 = ''
            for _ in range(self.tsize):
                randomStr1 = randomStr1 + chr(randint(MIN_ASCII, MAX_ASCII))
                randomStr2 = randomStr2 + chr(randint(MIN_ASCII, MAX_ASCII))
            member1 = GAstruct(randomStr1, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member2 = GAstruct(randomStr2, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            self.population.append(member1)
            self.nextPopulation.append(member2)

    def calcStringFitness(self, string1, string2):  # returns the string with better fitness
        if self.fitnessType == FitnessType.CHARACTER_DISTANCE:
            if self.characterDistanceFitness(string1) < self.characterDistanceFitness(string2):
                return string1
            else:
                return string2
        else:
            if self.bullseyeFitness(string1) < self.bullseyeFitness(string2):
                return string1
            else:
                return string2

    def calcFitness(self):  # loops on all members and calculates their fitness
        self.susInitArray = True
        sumFitness = 0
        if self.fitnessType == FitnessType.CHARACTER_DISTANCE:
            for person in self.population:
                fitness = self.characterDistanceFitness(person.getString())
                person.setFitness(fitness)
                sumFitness += fitness
        else:
            for person in self.population:
                fitness = self.bullseyeFitness(person.getString())
                person.setFitness(fitness)
                sumFitness += fitness

    def characterDistanceFitness(self, string):
        fitness = 0
        for j in range(0, self.tsize):
            fitness += abs(ord(string[j]) - ord(self.args.GA_TARGET[j]))
        return fitness

    def bullseyeFitness(self, string):
        fitness = 0
        for i in range(0, self.tsize):
            char = string[i]
            if char == self.args.GA_TARGET[i]:
                fitness += 0
            elif char in self.args.GA_TARGET:
                fitness += 30
            else:
                fitness += 80
        return fitness

    def mutate(self, member):
        tsize = len(self.args.GA_TARGET)
        ipos = randint(0, tsize - 1)
        string = member.getString()
        member.setString(string[:ipos] +
                         chr(randint(MIN_ASCII, MAX_ASCII)) + string[ipos + 1:])

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

            str1 = person1.getString()
            str2 = person2.getString()
            string1 = str1[0: spos] + str2[spos:]
            string2 = str2[0: spos] + str1[spos:]

            string = self.calcStringFitness(string1, string2)
            member = GAstruct(string, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def twoPointCrossover(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            spos1 = randint(0, self.tsize - 2)
            spos2 = randint(spos1 + 1, self.tsize - 1)

            person1, person2 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)

            str1 = person1.getString()
            str2 = person2.getString()
            string1 = str1[0: spos1] + str2[spos1: spos2] + str1[spos2:]
            string2 = str2[0: spos1] + str1[spos1: spos2] + str2[spos2:]

            string = self.calcStringFitness(string1, string2)
            member = GAstruct(string, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def uniformCrossover(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            person1, person2 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)

            string1 = ''
            string2 = ''

            str1 = person1.getString()
            str2 = person2.getString()

            for j in range(0, self.tsize):
                if (int(random()) % 2) == 0:
                    string1 = string1 + str1[j]
                    string2 = string2 + str2[j]
                else:
                    string1 = string1 + str2[j]
                    string2 = string2 + str1[j]

            string = self.calcStringFitness(string1, string2)
            member = GAstruct(string, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)
