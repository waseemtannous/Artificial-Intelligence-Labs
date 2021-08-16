from lab4 import CVRP_INPUT
from lab4.GeneticAlgorithm import *
from lab4.MultiKnapsack import *
from lab4.Sack import *


def getInput() -> MultiKnapsackProblem:
    file = open('ARGS\\MULTI_KNAPSACK_ARGS.txt', 'r')

    line = file.readline()
    arr = [num for num in line.split()]
    string = str(arr[2])

    line = file.readline()
    arr = [num for num in line.split()]
    if int(arr[2]) == 1:
        fitness = 0
    else:
        fitness = 1

    file.close()
    file = open('INPUT\\multiKnapsack\\' + string, 'r')
    line = file.readline()
    arr = [int(num) for num in line.split()]
    numberOfObjects = arr[1]
    values = []
    while len(values) != numberOfObjects:
        line = file.readline()
        arr = [int(num) for num in line.split()]
        for i in range(len(arr)):
            values.append(arr[i])

    line = file.readline()
    arr = [int(num) for num in line.split()]  # capacity of sacks
    sacks = []
    sumDensities: dict = {}
    for i in range(len(arr)):
        weights = []
        while len(weights) != numberOfObjects:
            line = file.readline()
            line = line.strip()
            temp = [int(num) for num in line.split()]
            for j in range(len(temp)):
                weights.append(temp[j])
        sack = Sack(arr[i])
        sacks.append(sack)
        for j in range(len(weights)):
            object = Object(j, values[j], weights[j])
            sack.addObject(object)

    for sack in sacks:
        sack.sumDensities(sumDensities)

    sumDensities = {k: v for k, v in sorted(sumDensities.items(), key=lambda item: item[1])}

    line = file.readline()
    while line == '\n':
        line = file.readline()
    optimum = int(line.strip())
    return MultiKnapsackProblem(sacks, optimum, values, sumDensities, len(values), fitness)


def cvrp(problemNum):
    startTime = time.time()
    cvrp = CVRP_INPUT.getInput(problemNum)
    cvrp.divideVehicles()
    args = CVRP_INPUT.getTabuArgs()
    cvrp.solveTsp(args)
    print('Time elapsed: ', time.time() - startTime)


def mks():
    startTime = time.time()
    multiKnapsackProblem = getInput()
    multiKnapsack(multiKnapsackProblem)
    print('Time elapsed: ', time.time() - startTime)


def nsga(problemNum):
    startTime = time.time()
    cvrp = CVRP_INPUT.getInput(problemNum)
    args = getGaArgs(len(cvrp.cities))
    GA = GeneticAlgorithm(args, cvrp)
    GA.run()
    print('Time elapsed: ', time.time() - startTime)


def getGaArgs(lenNodes):
    file = open('ARGS\\GA_ARGS.txt', 'r')  # input string

    line = file.readline()
    arr = [num for num in line.split(' ')]
    popsize = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxIter = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    mutationRate = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    tournamentK = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    linearA = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    linearB = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    localOptMax = int(arr[2])

    cross, sel, mut = None, None, None

    cross = CrossoverType.PMX

    line = file.readline()
    arr = [num for num in line.split(' ')]
    selection = int(arr[2])
    if selection == 1:
        sel = SelectionType.RWS

    line = file.readline()
    arr = [num for num in line.split(' ')]
    selection = int(arr[2])
    if selection == 1:
        sel = SelectionType.SUS

    line = file.readline()
    arr = [num for num in line.split(' ')]
    selection = int(arr[2])
    if selection == 1:
        sel = SelectionType.TOURNAMENT

    line = file.readline()
    arr = [num for num in line.split(' ')]
    mutation = int(arr[2])
    if mutation == 1:
        mut = MutationType.EXCHANGE

    line = file.readline()
    arr = [num for num in line.split(' ')]
    mutation = int(arr[2])
    if mutation == 1:
        mut = MutationType.SIMPLE_INVERSION

    args = GaArgs(popsize, maxIter, 0, mutationRate,
                  tournamentK, 0, 0, lenNodes, linearA, linearB, localOptMax,
                  cross, sel, mut)
    return args


if __name__ == '__main__':
    print('You can edit the arguments files found in \'ARGS\' folder.')
    print('Enter the number of the algorithm you want to run:')
    print('1 - multi-knapsack')
    print('2 - CVRP with multi-knapsack and tsp')
    print('3 - CVRP with NSGA-2')
    algo = int(input())
    if algo == 1:
        mks()
    elif algo == 2:
        print('Enter the problem number you want to run: 1-7')
        problemNum = str(input())
        cvrp(problemNum)
    elif algo == 3:
        print('Enter the problem number you want to run: 1-7')
        problemNum = str(input())
        nsga(problemNum)
    # mks()
    # cvrp()
    # nsga()
