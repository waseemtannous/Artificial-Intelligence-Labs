from lab4.GAstruct import GAstruct
from random import random
from lab4.Functions import *
from math import sqrt
from lab4.Variables import *
from random import randint
from numpy.random import choice
import time
from lab4.Front import *


class GeneticAlgorithm:

    def __init__(self, args, CVRP):
        self.args = args
        self.crossoverType = args.CROSS
        self.mutationType = args.MUTATION
        self.selectionType = args.SELECTION
        self.population = []
        self.nextPopulation = []
        self.CVRP = CVRP
        self.w1 = 0.5
        self.w2 = 0.5

    def run(self):
        startTime = time.time()
        self.initPopulation()
        paretoOptimal = []
        globalBest = None

        for _ in range(self.args.GA_MAXITER):
            iterTime = time.time()
            self.nextPopulation = []
            self.calcFitness()
            try:
                self.mate()
            except:
                break
            self.calcFitness()
            fronts = self.nonDominatedSorting()
            paretoOptimal = fronts[0].members
            self.getNextPopulation(fronts)
            paretoOptimal.sort()
            localBest = paretoOptimal[0]
            if globalBest is None:
                globalBest = localBest

            if localBest.fitness < globalBest.fitness:
                globalBest = localBest
            print(f'Global Best:   --fitness = {globalBest.fitness},  '
                  f'--number of vehicles = {globalBest.numberOfVehicles},  '
                  f'--path cost = {globalBest.pathCost},  ')

            print('Generation time: ', time.time() - iterTime)
            print()
        print('Time elapsed: ', time.time() - startTime)
        print(f'Best:   --fitness = {globalBest.fitness},  '
              f'--number of vehicles = {globalBest.numberOfVehicles},  '
              f'--path cost = {globalBest.pathCost},  ')
        self.CVRP.printSolution(globalBest)

    def initPopulation(self):
        for _ in range(self.args.GA_POPSIZE):
            randomStr1 = GAGreedySol(self.args.SIZE, self.CVRP)
            randomStr2 = GAGreedySol(self.args.SIZE, self.CVRP)

            member1 = GAstruct(randomStr1, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            member2 = GAstruct(randomStr2, 0, self.args.AGE_MIN, self.args.AGE_MAX)
            self.population.append(member1)
            self.nextPopulation.append(member2)

    def getNextPopulation(self, fronts):
        size = self.args.GA_POPSIZE
        self.population = []
        for front in fronts:
            if len(front.members) <= size:
                size -= len(front.members)
                front.addMembersToPopulation(self.population, len(front.members))
            else:
                front.crowdingDistanceSorting()
                front.addMembersToPopulation(self.population, size)
                break

    def nonDominatedSorting(self):
        size = len(self.population)
        for i in range(size):
            for j in range(size):
                if i == j:
                    continue
                self.domination(self.population[i], self.population[j])
        fronts = []
        while len(self.population) > 0:
            front = Front()
            front.addMembersToFront(self.population)
            fronts.append(front)
        return fronts

    # check if member1 dominates member2
    def domination(self, member1: GAstruct, member2: GAstruct):
        if ((member1.pathCost <= member2.pathCost) and (member1.numberOfVehicles <= member2.numberOfVehicles)) \
                and ((member1.pathCost < member2.pathCost) or (member1.numberOfVehicles < member2.numberOfVehicles)):
            member1.dominates.append(member2)
            member2.dominationCount += 1

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

        for i in range(self.args.GA_POPSIZE):
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
            self.population.append(member)

    def OX(self):
        agePopulation, scaledFitness, sumScalledFitness = self.scaleFitness()
        for i in range(self.args.GA_POPSIZE):
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
            self.population.append(member)

    def calcStringFitness(self, string1, string2):
        if self.pathCost(string1) < self.pathCost(string2):
            return string1
        else:
            return string2

    def pathCost(self, string):
        pathCost, numberOfVehicles = self.CVRP.calcPathCost(string)
        return (self.w1 * pathCost) + (self.w2 * numberOfVehicles * numberOfVehicles)

    def calcFitness(self):
        for person in self.population:
            person.setFitness(self.pathCost(person.getString()))
            pathCost, numberOfVehicles = self.CVRP.calcPathCost(person.string)
            person.numberOfVehicles = numberOfVehicles
            person.pathCost = pathCost

    def mutate(self, member):
        if self.mutationType == MutationType.EXCHANGE:
            self.exchangeMutation(member)
        else:
            self.simpleInversionMutation(member)

    def mate(self):
        if self.crossoverType == CrossoverType.PMX:
            self.PMX()
        else:
            self.OX()

    def sortByFitness(self):
        self.population.sort()

    def scaleFitness(self):  # scales the fitness and uses it to make a probability vector
        scaled = []
        agePopulation = []
        sum = 0
        for person in self.population:
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
