import time
from lab3.Variables import *


def tabuSearch(constraints, domains, args, assignment, fitnessType, neighborhoodType, maxTime, globalStartTime):
    startTime = time.time()
    best = assignment
    conflictNodes, bestFitness = getFitness(best, domains, fitnessType)
    bestCandidate = best
    globalBest = best
    globalFitness = bestFitness
    tabuDict = {str(best): True}
    tabu = [best]
    local_counter = 0
    for i in range(args.maxIter):
        if time.time() - globalStartTime > maxTime:
            break
        if bestFitness == 0:
            print('Time elapsed: ', time.time() - startTime)
            return globalBest, globalFitness
        iterTime = time.time()
        neighborhood = getNeighborhood(bestCandidate, args.numNeighbors, conflictNodes,
                                       domains[:], neighborhoodType)  # get neighborhood of current solution
        _, minimum = getFitness(best, domains, fitnessType)
        bestCandidate = neighborhood[0]
        for neighbor in neighborhood:  # get the best neighbor and save it
            tempConflictNodes, cost = getFitness(neighbor, domains, fitnessType)
            if cost < minimum and not tabuDict.get(str(neighbor), False):
                minimum = cost
                bestCandidate = neighbor
                conflictNodes = tempConflictNodes
        if minimum < bestFitness:  # update best (take a step towards the better neighbor)
            bestFitness = minimum
            best = bestCandidate
            local_counter = 0
        elif minimum == bestFitness:  # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness:  # update the best solution found until now
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
            bestCandidate = assignment
            best = bestCandidate
            conflictNodes, bestFitness = getFitness(assignment, domains, fitnessType)
            local_counter = 0
            tabuDict = {str(bestCandidate): True}
        print('Generation time: ', time.time() - iterTime)
        printSolution(best)
        print('cost = ', bestFitness)
        print()
    print('Time elapsed: ', time.time() - startTime)
    return globalBest, globalFitness


def getFitness(assignment, domains, fitnessType):
    if fitnessType == FitnessType.FEASIBLE:
        return numberOfConflicts(assignment)
    elif fitnessType == FitnessType.OBJECTIVE:
        return objectiveFitness(assignment, domains)
    else:
        return hybridFitness(assignment, domains)


def hybridFitness(assignment, domains):
    colorClasses = {}
    edgeClasses = {}
    for value in domains:
        colorClasses[value] = 0
        edgeClasses[value] = 0
    for node in assignment:
        colorClasses[assignment[node]] += 1
    for node in assignment:
        currentNodeColor = assignment[node]
        for neighbor in node.neighbors:
            if assignment[neighbor] == currentNodeColor:
                edgeClasses[currentNodeColor] += 1
    fitness = 0
    for value in domains:
        bi = edgeClasses[value]
        ci = colorClasses[value]
        fitness += (2 * bi * ci) - (ci ** 2)
    return None, fitness


def numberOfConflicts(assignment):  # fitness function
    conflictsNum = 0
    conflictNodes = []
    for node in assignment:
        currentNodeColor = assignment[node]
        for neighbor in node.neighbors:
            if assignment[neighbor] == currentNodeColor and neighbor not in conflictNodes:
                conflictsNum += 1
                conflictNodes.append(neighbor)
    return conflictNodes, conflictsNum


def objectiveFitness(assignment, domains):
    colorClasses = {}
    for value in domains:
        colorClasses[value] = 0
    for node in assignment:
        colorClasses[assignment[node]] += 1
    fitness = 0
    flag = False
    for value in colorClasses:
        if colorClasses[value] == 0:
            flag = True
        fitness += (colorClasses[value] ** 2)
    return flag, fitness


def getNeighborhood(origAssignment, numNeighbors, conflictNodes, domains, neighborhoodType):
    if neighborhoodType == NeighborhoodType.REGULAR:
        return regularNeighborhood(origAssignment, numNeighbors, conflictNodes, domains)
    else:
        return kempeNeighborhood(origAssignment, numNeighbors, domains)


def regularNeighborhood(origAssignment, numNeighbors, conflictNodes, domains):
    neighbors = []
    for _ in range(numNeighbors):
        assignment = {key: value for key, value in origAssignment.items()}  # deep copy
        minConflictsColor = [0 for _ in range(len(domains))]
        node = conflictNodes[random.randint(0, len(conflictNodes) - 1)]
        for neighbor in node.neighbors:
            minConflictsColor[origAssignment[neighbor] - 1] += 1
        minimum = float('inf')
        minimumColor = 0
        for i in range(len(minConflictsColor)):
            if minConflictsColor[i] < minimum:
                minimum = minConflictsColor[i]
                minimumColor = i + 1
        if random.random() < 0.5:
            assignment[node] = minimumColor
        else:
            assignment[node] = domains[random.randint(0, len(domains) - 1)]
        neighbors.append(assignment)
    return neighbors


def kempeNeighborhood(origAssignment, numNeighbors, domains):
    colorClasses = {}
    for value in domains:
        colorClasses[value] = []
    for node in origAssignment:
        colorClasses[origAssignment[node]].append(node)
    minValue = None
    minNumber = float('inf')
    for value in domains:
        if len(colorClasses[value]) < minNumber:
            minNumber = len(colorClasses[value])
            minValue = value
    nodesByColor = colorClasses[minValue]

    domains.remove(minValue)

    neighbors = []
    for _ in range(numNeighbors):
        assignment = {key: value for key, value in origAssignment.items()}  # deep copy
        node = nodesByColor[random.randint(0, len(nodesByColor) - 1)]
        oldColor = assignment[node]
        assignment[node] = domains[random.randint(0, len(domains) - 1)]
        newColor = assignment[node]
        kempeChain(assignment, node, oldColor, newColor)
        neighbors.append(assignment)
    return neighbors


def kempeChain(assignment, node, oldColor, newColor):
    queue = [node]
    hashTable = {}
    while len(queue) > 0:
        currentNode = queue.pop(0)
        if assignment[currentNode] == oldColor:
            assignment[currentNode] = newColor
        elif assignment[currentNode] == newColor:
            assignment[currentNode] = oldColor
        hashTable[currentNode] = True
        for neighbor in currentNode.neighbors:
            if not hashTable.get(neighbor, False):
                queue.append(neighbor)
    return assignment