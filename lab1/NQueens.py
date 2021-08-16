from lab1.GAstruct import GAstruct
from random import random, shuffle
from lab1.Functions import *


class NQueens:

    def __init__(self, args):
        self.args = args
        self.crossoverType = args.CROSS
        self.mutationType = args.MUTATION
        self.selectionType = args.SELECTION
        self.esize = int(self.args.GA_ELITRATE * self.args.GA_POPSIZE)
        self.population = []
        self.nextPopulation = []
        self.susPopulation = []
        self.susInitArray = True
        self.susIndex = 0

    def initPopulation(self):
        for _ in range(self.args.GA_POPSIZE):
            randomStr1 = [i for i in range(0, self.args.NQUEENS)]
            randomStr2 = [i for i in range(0, self.args.NQUEENS)]

            shuffle(randomStr1)
            shuffle(randomStr2)

            member1 = GAstruct(randomStr1, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member2 = GAstruct(randomStr2, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            self.population.append(member1)
            self.nextPopulation.append(member2)

    def exchangeMutation(self, person):
        string = person.getString()
        i1 = randint(0, self.args.NQUEENS - 1)
        i2 = randint(0, self.args.NQUEENS - 1)
        string[i1], string[i2] = string[i2], string[i1]
        person.setString(string)

    def simpleInversionMutation(self, person):
        string = person.getString()
        i1 = randint(0, self.args.NQUEENS - 1)
        i2 = randint(0, self.args.NQUEENS - 1)
        if i1 > i2:
            i1, i2 = i2, i1
        while i1 < i2:
            string[i1], string[i2] = string[i2], string[i1]
            i1 += 1
            i2 -= 1
        person.setString(string)

    def PMX(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)

        for i in range(self.esize, self.args.GA_POPSIZE):
            pmx = randint(0, self.args.NQUEENS - 1)
            person1, person2 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)

            father = person1.getString()[0:]
            mother = person2.getString()[0:]

            num1 = father[pmx]
            num2 = mother[pmx]

            for i in range(len(father)):
                if father[i] == num2:
                    father[i], father[pmx] = num1, father[i]
                    break
            for i in range(len(mother)):
                if mother[i] == num1:
                    mother[i], mother[pmx] = num2, mother[i]
                    break
            string = self.calcStringFitness(father, mother)
            member = GAstruct(string, self.collosionFitness(string), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def OX(self):
        agePopulation, scaledFitness, sumScalledFitness = scaleFitness(self)
        for i in range(self.esize, self.args.GA_POPSIZE):
            numbers_father = [i for i in range(0, self.args.NQUEENS - 1)]
            maxIndex = len(numbers_father) - 1
            index_father = []
            index_mother = []
            father1, mother1 = getCouple(self, agePopulation, scaledFitness, sumScalledFitness)
            father = father1.getString()
            mother = mother1.getString()
            for _ in range(int(self.args.NQUEENS / 2)):  # choose wich indexes we want to take from father
                randI1 = randint(0, maxIndex)
                index_father.append(numbers_father[randI1])
                numbers_father[randI1], numbers_father[maxIndex] = numbers_father[maxIndex], numbers_father[randI1]
                maxIndex -= 1

            index_father.sort()
            NonDuplicat_index = []

            for i in range(len(index_father)):
                NonDuplicat_index.append(father[index_father[i]])
            NonDuplicat_index.sort()

            k1 = 0
            for i in range(int(self.args.NQUEENS)):
                if k1 < len(NonDuplicat_index) and i == NonDuplicat_index[k1]:
                    k1 += 1
                else:
                    for l in range(len(mother)):
                        if mother[l] == i:
                            index_mother.append(l)
                            break
            index_mother.sort()
            child = []
            k1 = 0
            k2 = 0

            for i in range(self.args.NQUEENS):
                if k1 < len(index_father) and i == index_father[k1]:
                    child.append(father[i])
                    k1 += 1
                else:
                    child.append(mother[index_mother[k2]])
                    k2 += 1

            member = GAstruct(child, self.collosionFitness(child), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def calcStringFitness(self, string1, string2):
        if self.collosionFitness(string1) < self.collosionFitness(string2):
            return string1
        else:
            return string2

    def collosionFitness(self, string):
        fitness = 0
        for i in range(self.args.NQUEENS):
            for j in range(self.args.NQUEENS):
                if i != j and abs(
                        int(string[i]) - int(string[j]) == abs(i - j)):  # check if there are queens in diagonal
                    fitness += 1
        return fitness

    def calcFitness(self):
        for person in self.population:
            person.setFitness(self.collosionFitness(person.getString()))

    def mutate(self, member):
        if self.mutationType == MutationType.EXCHANGE:
            self.exchangeMutation(member)
        else:
            self.simpleInversionMutation(member)

    def mate(self):
        elitism(self)

        if self.crossoverType == CrossoverType.PMX:
            self.PMX()
        else:
            self.OX()
