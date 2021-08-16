from math import pow
from random import randint
from numpy.random import choice
import time


def ACO(problem, args):
    startTime = time.time()
    pheremonMatrix = [[float(1000) for _ in range(problem.size)] for _ in range(problem.size)]
    bestPath = []
    bestFitness = float('inf')
    currentBestPath = []
    currentBestFitness = float('inf')
    globalBest = []
    globalFitness = float('inf')
    local_counter = 0
    for _ in range(args.maxIter):
        iterTime = time.time()
        tempPath = getPath(problem, pheremonMatrix, args)
        tempFitness, _ = problem.calcPathCost(tempPath)
        if tempFitness < currentBestFitness:
            currentBestFitness = tempFitness
            currentBestPath = tempPath
        if currentBestFitness < bestFitness:  # update best (take a step towards the better neighbor)
            bestFitness = currentBestFitness
            bestPath = currentBestPath
            local_counter = 0
        if currentBestFitness == bestFitness:   # to detect local optimum
            local_counter += 1
        if bestFitness < globalFitness:# update the best solution found untill now
            globalBest = bestPath
            globalFitness = bestFitness
        updatePheremons(pheremonMatrix, tempPath, tempFitness, args.q, args.p)
        print('Generation time: ', time.time() - iterTime)
        print('sol = ', bestPath)
        print('cost = ', bestFitness)
        print()
        if local_counter == args.localOptStop:  # if fallen into local optimum, reset and continue with the algorithm
            pheremonMatrix = [[float(1000) for _ in range(problem.size)] for _ in range(problem.size)]
            local_counter = 0
            if bestFitness < globalFitness:
                globalBest = bestPath
                globalFitness = bestFitness
            bestPath = []
            bestFitness = float('inf')
            currentBestPath = []
            currentBestFitness = float('inf')
    print('Time elapsed: ', time.time() - startTime)
    problem.best = globalBest   # save the solution and its fitness
    problem.bestFitness = globalFitness


def getPath(problem, pheremonMatrix, args):
    cities = [i + 1 for i in range(problem.size)]
    probMatrix = []
    for i in range(problem.size):
        arrayProb = []
        for j in range(problem.size):
            num = 0
            if i != j:
                num = calculateProb(i, j, pheremonMatrix, problem.distanceMatrix, args.a, args.b)
            arrayProb.append(num)
        probMatrix.append(arrayProb)
    currentCity = randint(1, len(cities))
    cities[currentCity - 1] = -1
    path = [currentCity]
    while len(cities) != len(path):
        probVect = getProbVector(currentCity, probMatrix)
        updateProbMatrix(currentCity, probMatrix)
        currentCity = choice(cities, p=probVect)
        cities[currentCity - 1] = -1
        path.append(currentCity)
    return path


def calculateProb(i, j, pheremonMatrix, distanceMatrix, a, b):
    tau = float(pheremonMatrix[i][j])
    n = float(1 / float(distanceMatrix[i + 1][j + 1]))
    return float(pow(tau, a) * pow(n, b))


def getProbVector(currentCity, probMatrix):
    vector = []
    arr = probMatrix[currentCity - 1][:]
    probSum = sum(arr)
    for i in range(len(probMatrix[0])):
        vector.append(float(float(probMatrix[currentCity - 1][i]) / float(probSum)))
    return vector


def updateProbMatrix(currentCity, probMatrix):
    for i in range(len(probMatrix[0])):
        probMatrix[currentCity - 1][i] = float(0)
        probMatrix[i][currentCity - 1] = float(0)


def updatePheremons(pheremonMatrix, bestPath, pathCost, q, p):
    currentPheremons = [[float(0) for _ in range(len(pheremonMatrix[0]))] for _ in range(len(pheremonMatrix[0]))]
    for i in range(len(bestPath) - 1):
        currentPheremons[bestPath[i] - 1][bestPath[i + 1] - 1] = float(float(q) / float(pathCost))
        currentPheremons[bestPath[i + 1] - 1][bestPath[i] - 1] = float(float(q) / float(pathCost))

    for i in range(len(pheremonMatrix[0])):
        for j in range(len(pheremonMatrix[0])):
            num1 = float(pheremonMatrix[i][j] * (1 - p))
            num2 = float(currentPheremons[i][j] * p)
            pheremonMatrix[i][j] = float(num1 + num2)
            if pheremonMatrix[i][j] < 0.0001:
                pheremonMatrix[i][j] = 0.0001



# 1 [383.84103229415234, 383.84103229415234, 383.84103229415246, 383.84103229415234, 383.84103229415234, 383.8410322941523, 383.84103229415234, 383.84103229415234, 383.84103229415234, 383.84103229415234]
# 2 [895.0827298826225, 895.0301202308657, 896.5865308727716, 895.146464019747, 892.7863629697499, 899.2508136946292, 877.3888317091088, 899.8627858794197, 889.2336129358667, 895.8723512510296]
# 3 [614.6724373933889, 618.4529825203196, 621.3077377676718, 646.9658434973543, 639.3058597596058, 622.9239631273259, 627.1054577397429, 612.4405913505414, 621.5292229220787, 620.5167363739248]
# 4 [929.5122711284135, 935.7985490501742, 956.4584845357108, 932.933919937869, 946.0050522764964, 940.2963147504303, 927.7866134691815, 953.1780006205569, 963.2981888745861, 924.8178676506462]
# 5 [835.6515093817123, 843.4188142958476, 846.6090790700962, 842.6820499351774, 843.2503385984894, 844.9619667444922, 833.8703150578018, 831.5983936594059, 828.8095709811585, 854.900423588134]
# 6 [1017.482867679543, 1025.3728602978797, 1018.1113208620151, 1011.3570666858634, 1015.9859072228709, 982.5986912661695, 1031.4441248356236, 940.3802359768042, 979.1493952032063, 1018.6279484264867]
# 7 [1267.0809567311453, 1263.0002966637417, 1264.9783602049463, 1287.7896448853526, 1288.7224193244965, 1282.8369845469028, 1253.4421455850188, 1269.4414278123802, 1269.9897223819125, 1299.7256714595499]
