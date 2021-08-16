from lab2.GAstruct import GAstruct
from random import random, shuffle
from lab2.Functions import *
from math import sqrt
from lab2.Variables import *
from random import randint
from numpy.random import choice
import time


class GeneticAlgorithm:

    def __init__(self, args, CVRP):
        self.args = args
        self.crossoverType = args.CROSS
        self.mutationType = args.MUTATION
        self.selectionType = args.SELECTION
        self.esize = int(self.args.GA_ELITRATE * self.args.GA_POPSIZE)
        self.population = []
        self.nextPopulation = []
        self.CVRP = CVRP

    def run(self):
        startTime = time.time()
        self.initPopulation()

        repeat = 0
        bestFitness = float('inf')

        best = []
        genBestFit = 0

        for _ in range(self.args.GA_MAXITER):
            iterTime = time.time()
            self.calcFitness()
            self.sortByFitness()
            self.printBest()
            self.calcAvgSd()

            # this checks if we have reached a local optimum or found the goal
            if repeat == self.args.LOCAL_STOP_ITER or self.population[0].getFitness() == 0:
                print('Generation time: ', time.time() - iterTime)
                print()
                break

            best = self.population[0].getString()[:]
            genBestFit = self.population[0].getFitness()

            if bestFitness == genBestFit:
                repeat += 1
            elif genBestFit < bestFitness:
                bestFitness = genBestFit
                repeat = 1

            self.mate()
            try:
                pass
            except:
                print('Generation time: ', time.time() - iterTime)
                break
            self.swap()
            self.aging()
            print('Generation time: ', time.time() - iterTime)
            print()
        print('Time elapsed: ', time.time() - startTime)
        self.CVRP.best = best
        self.CVRP.bestFitness = genBestFit

    def initPopulation(self):
        for _ in range(self.args.GA_POPSIZE):
            randomStr1 = initGreedySol(self.args.SIZE, self.CVRP)
            randomStr2 = initGreedySol(self.args.SIZE, self.CVRP)

            member1 = GAstruct(randomStr1, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member2 = GAstruct(randomStr2, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            self.population.append(member1)
            self.nextPopulation.append(member2)

    def exchangeMutation(self, person):
        string = person.getString()
        i1 = randint(0, self.args.SIZE - 1)
        i2 = randint(0, self.args.SIZE - 1)
        string[i1], string[i2] = string[i2], string[i1]
        person.setString(string)

    def simpleInversionMutation(self, person):
        string = person.getString()
        i1 = randint(0, self.args.SIZE - 1)
        i2 = randint(0, self.args.SIZE - 1)
        if i1 > i2:
            i1, i2 = i2, i1
        while i1 < i2:
            string[i1], string[i2] = string[i2], string[i1]
            i1 += 1
            i2 -= 1
        person.setString(string)

    def PMX(self):
        agePopulation, scaledFitness, sumScalledFitness = self.scaleFitness()

        for i in range(self.esize, self.args.GA_POPSIZE):
            pmx = randint(0, self.args.SIZE - 1)
            person1, person2 = self.getCouple(agePopulation, scaledFitness, sumScalledFitness)

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
            member = GAstruct(string, self.pathCost(string), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def OX(self):
        agePopulation, scaledFitness, sumScalledFitness = self.scaleFitness()
        for i in range(self.esize, self.args.GA_POPSIZE):
            numbers_father = [i for i in range(0, self.args.SIZE - 1)]
            maxIndex = len(numbers_father) - 1
            index_father = []
            index_mother = []
            father1, mother1 = self.getCouple(agePopulation, scaledFitness, sumScalledFitness)
            father = father1.getString()
            mother = mother1.getString()
            for _ in range(int(self.args.SIZE / 2)):  # choose wich indexes we want to take from father
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
            for i in range(int(self.args.SIZE)):
                if k1 < len(NonDuplicat_index) and (i + 1) == NonDuplicat_index[k1]:
                    k1 += 1
                else:
                    for l in range(len(mother)):
                        if mother[l] == i + 1:
                            index_mother.append(l)
                            break
            index_mother.sort()
            child = []
            k1 = 0
            k2 = 0

            for i in range(self.args.SIZE):
                if k1 < len(index_father) and i == index_father[k1]:
                    child.append(father[i])
                    k1 += 1
                elif k2 < len(index_mother):
                    child.append(mother[index_mother[k2]])
                    k2 += 1

            member = GAstruct(child, self.pathCost(child), self.args.AGE_MIN, self.args.AGE_MAX)
            member.zeroAge()

            if random.random() < self.args.GA_MUTATION:
                self.mutate(member)
            self.nextPopulation.append(member)

    def calcStringFitness(self, string1, string2):
        if self.pathCost(string1) < self.pathCost(string2):
            return string1
        else:
            return string2

    def pathCost(self, string):
        fitness, _ = self.CVRP.calcPathCost(string)
        return fitness

    def calcFitness(self):
        for person in self.population:
            person.setFitness(self.pathCost(person.getString()))

    def mutate(self, member):
        if self.mutationType == MutationType.EXCHANGE:
            self.exchangeMutation(member)
        else:
            self.simpleInversionMutation(member)

    def mate(self):
        self.elitism(self)

        if self.crossoverType == CrossoverType.PMX:
            self.PMX()
        else:
            self.OX()

    def elitism(self, problem):  # gets members that have the best fitness
        y = 0
        i = 0
        while i < problem.esize + y:
            if i == problem.args.GA_POPSIZE:
                break
            if problem.population[i].getAge() > problem.args.AGE_MAX:
                i += 1
                y += 1
                continue
            problem.nextPopulation.append(problem.population[i])
            i += 1

    def sortByFitness(self):
        self.population.sort()

    def scaleFitness(self):  # scales the fitness and uses it to make a probability vector
        scaled = []
        agePopulation = []
        sum = 0
        for person in self.population:
            if not person.isGoodForMating():
                continue
            num = (self.args.LINEAR_SCALING_A * person.getFitness()) + self.args.LINEAR_SCALING_B
            num = float(1 / num)
            sum += num
            agePopulation.append(person)
            scaled.append(num)
        for i in range(len(scaled)):
            scaled[i] = float(scaled[i] / sum)
        return agePopulation, scaled, sum

    def getCouple(self, agePopulation, scaledFitness, sumScalledFitness):  # returns 2 members for crossover
        person1, person2 = None, None
        if self.selectionType is SelectionType.RWS:
            person1 = self.RWS(agePopulation, scaledFitness)
            person2 = self.RWS(agePopulation, scaledFitness)
        elif self.selectionType is SelectionType.SUS:
            keep = self.SUS(agePopulation, scaledFitness)
            person1, person2 = keep[0], keep[1]
        else:
            person1 = self.tournamentSelection(agePopulation)
            person2 = self.tournamentSelection(agePopulation)
        return person1, person2

    def printBest(self):  # prints the member wih best fitness in the generation
        bestMember = self.population[0]
        print('Best: ', bestMember.getString(), ' (', bestMember.getFitness(), ')', end=" ")

    def swap(self):  # swaps populations for next generation
        self.population, self.nextPopulation = self.nextPopulation, self.population

    def calSumFitness(self):  # calculates the sum of the fitness of all members
        sumFitness = 0
        for person in self.population:
            sumFitness += person.getFitness()
        return sumFitness

    def calcAvgSd(self):  # calculates the average and the standard deviation
        sumFitness = self.calSumFitness()
        avg = sumFitness / self.args.GA_POPSIZE
        sum = 0
        for person in self.population:
            sum += (avg - person.getFitness()) ** 2
        sd = abs(sum / self.args.GA_POPSIZE)
        sd = sqrt(sd)
        print("fitness data:   avarage: ", avg, " || standard deviation:", sd)

    def RWS(self, population, scaledFitness):
        arr = [i for i in range(len(population))]
        index = choice(arr, p=scaledFitness)
        return population[index]

    def SUS(self, population, scaledFitnesses):
        indexArr = [i for i in range(int(len(population) / 2))]
        scaled = []
        sum = 0
        for i in range(int(len(population) / 2)):
            scaled.append(scaledFitnesses[i])
            sum += scaledFitnesses[i]

        for i in range(int(len(population) / 2)):
            scaled[i] = float(scaled[i] / sum)

        index1 = choice(indexArr, p=scaled)
        index2 = 2 * index1
        members = [population[index1], population[index2]]
        return members

    def tournamentSelection(self, population):
        best = None
        for _ in range(self.args.TOURNAMENT_K):
            person = population[randint(0, len(population) - 1)]
            if best is None:
                best = person
            elif best.getFitness() > person.getFitness():
                best = person
        return best

    def aging(self):
        for person in self.population:
            person.updateAge()
        self.nextPopulation.clear()
