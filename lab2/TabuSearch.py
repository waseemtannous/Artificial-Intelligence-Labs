from lab2.Functions import *
import time


def tabuSearch(problem, args):
    startTime = time.time()
    best = initGreedySol(problem.size, problem)
    bestFitness, _ = problem.calcPathCost(best)
    bestCandidate = best
    globalBest = best
    globalFitness = bestFitness
    tabuDict = {str(best): True}
    tabu = [best]
    local_counter = 0
    for _ in range(args.maxIter):
        iterTime = time.time()
        neighborhood = getNeighborhood(bestCandidate, args.numNeighbors)    # get neighborhood of current solution
        minimum, _ = problem.calcPathCost(neighborhood[0])
        bestCandidate = neighborhood[0]
        for neighbor in neighborhood:   # get the best neighbor and save it
            cost, _ = problem.calcPathCost(neighbor)
            if cost < minimum and not tabuDict.get(str(neighbor), False):
                minimum = cost
                bestCandidate = neighbor
        if minimum < bestFitness:   # update best (take a step towards the better neighbor)
            bestFitness = minimum
            best = bestCandidate
            local_counter = 0
        elif minimum == bestFitness:    # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness: # update the best solution found untill now
            globalBest = best
            globalFitness = bestFitness
        tabu.append(bestCandidate)
        tabuDict[str(bestCandidate)] = True
        if len(tabu) > args.maxTabu:
            tabuDict[str(tabu[0])] = False
            tabu.pop(0)
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            if bestFitness < globalFitness:
                globalBest = best
                globalFitness = bestFitness
            bestCandidate = initGreedySol(problem.size, problem)
            best = bestCandidate
            bestFitness, _ = problem.calcPathCost(best)
            local_counter = 0
            tabuDict = {str(bestCandidate): True}
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
    print('Time elapsed: ', time.time() - startTime)
    problem.best = globalBest   # save the solution and its fitness
    problem.bestFitness = globalFitness
