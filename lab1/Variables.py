import random
from enum import Enum

MIN_ASCII = 32
MAX_ASCII = 122

ENTRIES = []


class Arguments:  # this class holds all the arguments relevant to the problems
    def __init__(self, popsize, maxIter, eliteRate, mutationRate, targetString,
                 tournamentK, minAge, maxAge, N, linearA, linearB, localOptMax,
                 knapsackProblem, crossover, selection, mutation, fitness):
        self.GA_POPSIZE = popsize
        self.GA_MAXITER = maxIter
        self.GA_ELITRATE = eliteRate
        self.GA_MUTATIONRATE = mutationRate
        self.GA_MUTATION = random.random() * mutationRate
        self.GA_TARGET = targetString
        self.TOURNAMENT_K = tournamentK
        self.AGE_MIN = minAge
        self.AGE_MAX = maxAge
        self.NQUEENS = N
        self.LINEAR_SCALING_A = linearA
        self.LINEAR_SCALING_B = linearB
        self.LOCAL_STOP_ITER = localOptMax
        self.KNAPSACK_NUM = knapsackProblem
        self.CROSS = crossover
        self.SELECTION = selection
        self.MUTATION = mutation
        self.FITNESS = fitness




class CrossoverType(Enum):
    ONE_POINT = 1
    TWO_POINT = 2
    UNIFORM = 3
    PMX = 4
    OX = 5


class FitnessType(Enum):
    CHARACTER_DISTANCE = 1
    BULLSEYE = 2


class SelectionType(Enum):
    RWS = 1
    SUS = 2
    TOURNAMENT = 3


class MutationType(Enum):
    EXCHANGE = 1
    SIMPLE_INVERSION = 2
