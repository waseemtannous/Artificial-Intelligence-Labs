import random
from enum import Enum


ENTRIES = []

class Heuristic(Enum):
    MRV = 1
    MRV_HD = 2
    REGULAR = 3


class TabuArgs:
    def __init__(self, maxIter, localOptStop, maxTabu, numNeighbors):
        self.maxIter = maxIter
        self.localOptStop = localOptStop
        self.maxTabu = maxTabu
        self.numNeighbors = numNeighbors


def printSolution(solution: {}):
    print('Solution: {', end='')
    i = 0
    for node in solution:
        if i != 0:
            print(', ', end='')
        print(node.name, ':', solution[node], end='')
        i = 1
    print('}')


class GaArgs:  # this class holds all the arguments relevant to the problems
    def __init__(self, popsize, maxIter, eliteRate, mutationRate,
                 tournamentK, minAge, maxAge, N, linearA, linearB, localOptMax,
                 crossover, selection, mutation):
        self.GA_POPSIZE = popsize
        self.GA_MAXITER = maxIter
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATIONRATE = mutationRate
        self.GA_MUTATION = random.random() * mutationRate
        self.TOURNAMENT_K = tournamentK
        self.AGE_MIN = minAge
        self.AGE_MAX = maxAge
        self.SIZE = N
        self.LINEAR_SCALING_A = linearA
        self.LINEAR_SCALING_B = linearB
        self.LOCAL_STOP_ITER = localOptMax
        self.CROSS = crossover
        self.SELECTION = selection
        self.MUTATION = mutation


class CrossoverType(Enum):
    PMX = 1
    OX = 2


class SelectionType(Enum):
    RWS = 1
    SUS = 2
    TOURNAMENT = 3


class MutationType(Enum):
    EXCHANGE = 1
    SIMPLE_INVERSION = 2


class FitnessType(Enum):
    FEASIBLE = 1
    OBJECTIVE = 2
    HYBRID = 3


class NeighborhoodType(Enum):
    REGULAR = 1
    KEMPE = 2
