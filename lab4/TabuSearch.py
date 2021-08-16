from lab4.Functions import *
from lab4.Vehicle import *
import time


class TabuArgs:
    def __init__(self, maxIter, localOptStop, maxTabu, numNeighbors):
        self.maxIter = maxIter
        self.localOptStop = localOptStop
        self.maxTabu = maxTabu
        self.numNeighbors = numNeighbors


def tabuSearch(args: TabuArgs, vehicle: Vehicle, distanceMatrix, numOfVehicles):
    best = initGreedySol(vehicle.cities, distanceMatrix)
    bestFitness = calcPathCost(best, distanceMatrix)
    bestCandidate = best
    globalBest = best
    globalFitness = bestFitness
    tabuDict = {str(best): True}
    tabu = [best]
    local_counter = 0
    for _ in range(int(args.maxIter / numOfVehicles)):
        iterTime = time.time()
        neighborhood = getNeighborhood(bestCandidate, args.numNeighbors)  # get neighborhood of current solution
        minimum = calcPathCost(neighborhood[0], distanceMatrix)
        bestCandidate = neighborhood[0]
        for neighbor in neighborhood:  # get the best neighbor and save it
            cost = calcPathCost(neighbor, distanceMatrix)
            if cost < minimum and not tabuDict.get(str(neighbor), False):
                minimum = cost
                bestCandidate = neighbor
        if minimum < bestFitness:  # update best (take a step towards the better neighbor)
            bestFitness = minimum
            best = bestCandidate
            local_counter = 0
        elif minimum == bestFitness:  # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness:  # update the best solution found untill now
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
            bestCandidate = initGreedySol(vehicle.cities, distanceMatrix)
            best = bestCandidate
            bestFitness = calcPathCost(best, distanceMatrix)
            local_counter = 0
            tabuDict = {str(bestCandidate): True}
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', best)
        print('cost = ', bestFitness)
        print()
    globalBest.append(0)
    globalBest.insert(0, 0)
    vehicle.bestPath = globalBest
    vehicle.bestPathCost = globalFitness
