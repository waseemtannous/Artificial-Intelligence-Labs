from numpy import exp
from numpy.random import rand
from lab2.Functions import *
import time


def simulatedAnnealing(problem, args):
    startTime = time.time()
    best = initGreedySol(problem.size, problem)
    bestFitness, _ = problem.calcPathCost(best)
    globalBest = best
    globalFitness = bestFitness
    currentBest = best
    currentFitness = bestFitness
    temperature = float(args.temperature)
    local_counter = 0
    LK = 30
    for _ in range(args.maxIter):
        iterTime = time.time()
        neighborhood = getNeighborhood(best, args.numNeighbors)
        for _ in range(LK): # pick 'LK' neighbors and get the best
            randNeighbor = neighborhood[randint(0, len(neighborhood) - 1)]
            neighborFitness, _ = problem.calcPathCost(randNeighbor)
            diff = neighborFitness - bestFitness
            metropolis = float(exp(float(-1 * diff) / temperature))
            if neighborFitness < currentFitness or rand() < metropolis:
                currentFitness = neighborFitness
                currentBest = randNeighbor
        if currentFitness < bestFitness:   # update best (take a step towards the better neighbor)
            best = currentBest
            bestFitness = currentFitness
            local_counter = 0
        if currentFitness == bestFitness:    # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness: # update the best solution found untill now
            globalBest = best
            globalFitness = bestFitness
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            if bestFitness < globalFitness:
                globalBest = best
                globalFitness = bestFitness
            best = initGreedySol(problem.size, problem)
            bestFitness, _ = problem.calcPathCost(best)
            currentBest = best
            currentFitness = bestFitness
            local_counter = 0
            temperature = float(args.temperature)
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
        temperature *= args.alpha
    print('Time elapsed: ', time.time() - startTime)
    problem.best = globalBest   # save the solution and its fitness
    problem.bestFitness = globalFitness
