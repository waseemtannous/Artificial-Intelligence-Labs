from lab4.MultiKnapsackProblem import *

ARGS: MultiKnapsackProblem


def multiKnapsack(multiKnapsackProblem: MultiKnapsackProblem):
    global ARGS

    ARGS = multiKnapsackProblem
    length = multiKnapsackProblem.size
    for i in range(length):
        print('wave: ', i)
        lds(i)
        if ARGS.bestValue == ARGS.optimum:
            break

    print()
    print('best solution found:')
    print('vector: ', multiKnapsackProblem.bestVector, ', value: ', multiKnapsackProblem.bestValue)
    print('optimum: ', multiKnapsackProblem.optimum)
    if multiKnapsackProblem.bestValue == multiKnapsackProblem.optimum:
        print('reached optimum !!!!!!!!!')


def lds(numberOfZeros: int, vector=None) -> bool:
    if ARGS.bestValue == ARGS.optimum:
        return True

    if vector is None:
        vector = []
    if ARGS.deadEnd.get(str(vector), False):
        return False

    estimate, weights = checkVector(vector)

    if not weights or estimate <= ARGS.bestValue:
        ARGS.deadEnd[str(vector)] = True
        return False

    if len(vector) == ARGS.size:
        value = ARGS.sacks[0].calculateValue(vector)
        if value > ARGS.bestValue:
            ARGS.bestValue = value
            ARGS.bestVector = vector
            print('vector: ', ARGS.bestVector, ', value: ', ARGS.bestValue)
            return True
        return False

    vector0 = vector[:]
    vector0.append(0)
    vector1 = vector[:]
    vector1.append(1)

    if len(vector) + numberOfZeros == ARGS.size and numberOfZeros > 0:
        return lds(numberOfZeros - 1, vector0)
    elif numberOfZeros > 0:
        retVal1 = lds(numberOfZeros, vector1)
        retVal0 = lds(numberOfZeros - 1, vector0)
        return retVal0 or retVal1
    else:
        return lds(numberOfZeros, vector1)


def getEstimate(vector: list):
    if ARGS.fitness == 1:
        return integralItemSizes(vector)
    return unboundedWeight(vector)


def unboundedWeight(vector: list):
    estimate = ARGS.sumValues
    for i in range(len(vector)):
        if vector[i] == 0:
            estimate -= ARGS.values[i]
    return estimate


def integralItemSizes(vector: list):
    estimate = ARGS.sacks[0].calculateValue(vector)
    capacities = [sack.capacity for sack in ARGS.sacks]
    currentWeights = [sack.calculateWeight(vector) for sack in ARGS.sacks]
    minimumCut = 1
    for object, density in ARGS.sumDensities.items():
        if object.name < len(vector):
            if vector[object.name] == 0:
                continue
        for i in range(len(currentWeights)):
            currentWeights[i] -= object.weight
            estimate += object.value

    for object, density in ARGS.sumDensities.items():
        if object.name < len(vector):
            continue
        flag = False
        for i in range(len(currentWeights)):
            if currentWeights[i] - capacities[i] < 0 or flag:
                flag = True
                ratio = abs(float((currentWeights[i] - capacities[i]) / object.weight))
                minimumCut = min(minimumCut, ratio)
            else:
                currentWeights[i] -= object.weight
        if flag:
            estimate += float(object.value * minimumCut)
            return estimate
        estimate += object.value
    return estimate


def checkVector(vector: list):
    weightsFlag = True
    estimate = getEstimate(vector)
    if len(vector) == 0:
        return estimate, weightsFlag
    for sack in ARGS.sacks:
        weight = sack.calculateWeight(vector)
        if weight > sack.capacity:
            weightsFlag = False
            break
    return estimate, weightsFlag
