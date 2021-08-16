from math import sqrt
from lab1.Variables import *
from random import randint
from numpy.random import choice


def elitism(problem):   # gets members that have the best fitness
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


def sortByFitness(problem):
    problem.population.sort()


def scaleFitness(problem):  # scales the fitness and uses it to make a probability vector
    scaled = []
    agePopulation = []
    sum = 0
    for person in problem.population:
        if not person.isGoodForMating():
            continue
        num = (problem.args.LINEAR_SCALING_A * person.getFitness()) + problem.args.LINEAR_SCALING_B
        num = float(1 / num)
        sum += num
        agePopulation.append(person)
        scaled.append(num)
    for i in range(len(scaled)):
        scaled[i] = float(scaled[i] / sum)
    return agePopulation, scaled, sum


def getCouple(problem, agePopulation, scaledFitness, sumScalledFitness):    # returns 2 members for crossover
    person1, person2 = None, None
    if problem.selectionType is SelectionType.RWS:
        person1 = RWS(problem, agePopulation, scaledFitness)
        person2 = RWS(problem, agePopulation, scaledFitness)
    elif problem.selectionType is SelectionType.SUS:
        keep = SUS(problem, agePopulation, scaledFitness)
        person1, person2 = keep[0], keep[1]
    else:
        person1 = tournamentSelection(agePopulation, problem)
        person2 = tournamentSelection(agePopulation, problem)
    return person1, person2


def printBest(problem): # prints the member wih best fitness in the generation
    bestMember = problem.population[0]
    print('Best: ', bestMember.getString(), ' (', bestMember.getFitness(), ')', end=" ")


def swap(problem):  # swaps populations for next generation
    problem.population, problem.nextPopulation = problem.nextPopulation, problem.population


def calSumFitness(problem): # calculates the sum of the fitness of all members
    sumFitness = 0
    for person in problem.population:
        sumFitness += person.getFitness()
    return sumFitness


def calcAvgSd(problem): # calculates the average and the standard deviation
    sumFitness = calSumFitness(problem)
    avg = sumFitness / problem.args.GA_POPSIZE
    sum = 0
    for person in problem.population:
        sum += (avg - person.getFitness()) ** 2
    sd = abs(sum / problem.args.GA_POPSIZE)
    sd = sqrt(sd)
    print("fitness data:   avarage: ", avg, " || standard deviation:", sd)


def RWS(problem, population, scaledFitness):
    arr = [i for i in range(len(population))]
    index = choice(arr, p=scaledFitness)
    return population[index]


def SUS(problem, population, scaledFitnesses):
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


def tournamentSelection(population, problem):
    best = None
    for _ in range(problem.args.TOURNAMENT_K):
        person = population[randint(0, len(population) - 1)]
        if best is None:
            best = person
        elif best.getFitness() > person.getFitness():
            best = person
    return best


def aging(problem):
    for person in problem.population:
        person.updateAge()
    problem.nextPopulation.clear()
