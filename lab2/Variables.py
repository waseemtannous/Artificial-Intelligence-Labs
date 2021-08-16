import random
from enum import Enum

ENTRIES = []


class TabuArgs:
    def __init__(self, maxIter, localOptStop, maxTabu, numNeighbors):
        self.maxIter = maxIter
        self.localOptStop = localOptStop
        self.maxTabu = maxTabu
        self.numNeighbors = numNeighbors


class SimuArgs:
    def __init__(self, temperature, alpha, maxIter, localOptStop, numNeighbors):
        self.temperature = temperature
        self.alpha = alpha
        self.maxIter = maxIter
        self.localOptStop = localOptStop
        self.numNeighbors = numNeighbors


class ACOArgs:
    def __init__(self, maxIter, localOptStop, a, b, q, p):
        self.maxIter = maxIter
        self.localOptStop = localOptStop
        self.a = a
        self.b = b
        self.q = q
        self.p = p


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
