from lab3.CSP import *
from lab3.Constraint import *
from lab3.ConstraintsWrapper import *
from lab3.GeneticAlgorithm import *
from lab3.Node import *
from lab3.tabuSearch import *


def printGraphStats(v, e):
    density = float((2 * e) / (v * (v - 1)))  # which is also E / (V choose 2)
    print('Number of nodes: ', v)
    print('Number of edges: ', e)
    print('Graph Density = ', density)


def readFile(string):
    file = open(string, 'r')
    vertices = 0
    edges = 0
    edgesArray = []

    for line in file:
        arr = [char for char in line.split(' ')]
        if arr[0] == 'p':
            vertices = int(arr[2])
            edges = int(arr[3])
        if arr[0] == 'e':
            edgesArray.append((int(arr[1]), int(arr[2])))
            edgesArray.append((int(arr[2]), int(arr[1])))
    nodes = []
    for i in range(vertices):
        nodes.append(Node(i + 1))
    neighborsMatrix = [[0 for _ in range(vertices)] for _ in range(vertices)]

    constraintsByNode = {}
    allConstraints = []
    leftConstraints = {}
    rightConstraints = {}

    for edge in edgesArray:
        neighborsMatrix[edge[0] - 1][edge[1] - 1] = 1
        neighborsMatrix[edge[1] - 1][edge[0] - 1] = 1
        node1 = nodes[edge[0] - 1]
        node2 = nodes[edge[1] - 1]
        node1.addNeighbor(node2)
        node2.addNeighbor(node1)
        constraint = Constraint(node1, node2)
        if not constraintsByNode.get(constraint.node1, False):
            constraintsByNode[constraint.node1] = []
        if not constraintsByNode.get(constraint.node2, False):
            constraintsByNode[constraint.node2] = []
        if not leftConstraints.get(constraint.node1, False):
            leftConstraints[constraint.node1] = []
        if not rightConstraints.get(constraint.node2, False):
            rightConstraints[constraint.node2] = []

        constraintsByNode[constraint.node1].append(constraint)
        constraintsByNode[constraint.node2].append(constraint)
        leftConstraints[constraint.node1].append(constraint)
        rightConstraints[constraint.node2].append(constraint)
        allConstraints.append(constraint)

    constraintsWrapper = ConstraintsWrapper(constraintsByNode, allConstraints, leftConstraints, rightConstraints)

    variables = {}
    variables['constraintsWrapper'] = constraintsWrapper
    variables['vertices'] = vertices
    variables['edges'] = edges
    variables['nodes'] = nodes

    printGraphStats(variables['vertices'], variables['edges'])
    variables['greedyColors'], variables['greedyAssignment'] = greedyColoring(variables['nodes'], variables[
        'constraintsWrapper'].constraintsByNode)

    return variables


def chooseMostConstrainted(nodes, constraints):
    retNode = nodes[0]
    for node in nodes:
        if len(constraints[node]) > len(constraints[retNode]):
            retNode = node
    return retNode


def getNeighborsColors(node, assignment):
    colors = {}
    for neighbor in node.neighbors:
        if not assignment.get(neighbor, False):
            continue
        colors[assignment[neighbor]] = True
    return colors


def greedyColoring(nodes, constraints):
    localNodes = nodes.copy()
    assignment = {}
    domain = [1]
    for _ in range(len(localNodes)):
        currentColored = False
        node = chooseMostConstrainted(localNodes, constraints)
        localNodes.remove(node)
        neighborsColors = getNeighborsColors(node, assignment)
        for value in domain:
            if not neighborsColors.get(value, False):
                assignment[node] = value
                currentColored = True
                break
        if not currentColored:
            domain.append(domain[-1] + 1)
            assignment[node] = domain[-1]
    print()
    return len(domain), assignment


def checkSolutionConsistency(assignment, constraints):
    for node in constraints:
        for constraint in constraints[node]:
            if not constraint.isSatisfied(assignment):
                return False
    return True


def deleteColor(assignment, domains):
    colorClasses = {}
    for value in domains:
        colorClasses[value] = 0
    for node in assignment:
        colorClasses[assignment[node]] += 1
    minimum = float('inf')
    minValue = None
    for value in domains:
        num = colorClasses[value]
        if minimum > num:
            minimum = num
            minValue = value
    lastValue = domains[-1]
    if lastValue != minValue:
        for node in assignment:
            if assignment[node] == lastValue:
                assignment[node] = minValue
            elif assignment[node] == minValue:
                assignment[node] = random.randint(1, len(domains) - 1)
    else:
        for node in assignment:
            if assignment[node] == lastValue:
                assignment[node] = random.randint(1, len(domains) - 1)


def checkSol(assignment):
    for node in assignment:
        for neighbor in node.neighbors:
            if assignment[node] == assignment[neighbor]:
                return False
    return True


def runBacktracking(constraints, nodes, greedyColors, maxTime):
    print()
    startTime = time.time()
    for domainNumber in range(greedyColors - 1, 0, -1):
        for node in nodes:
            node.time = 0
        domains = {}
        print('Trying to color in  ', domainNumber, ' colors ... ', end='')
        for node in nodes:
            node.domains = [i + 1 for i in range(domainNumber)]
            node.initNeighborsColors()
            domains[node] = [i + 1 for i in range(domainNumber)]

        csp = CSP(startTime, maxTime, nodes, constraints, domains, [i + 1 for i in range(domainNumber)])
        solution = csp.backtracking()

        if solution is None:
            print("No solution found with ", domainNumber, ' colors.')
            print()
            print("Minimum number of colors needed is ", domainNumber + 1, ' colors.')
            print()
            break
        else:
            if checkSol(solution):
                print('Success !!')
                printSolution(solution)
            else:
                print("No solution found with ", domainNumber, ' colors.')
                print()
                print("Minimum colors needed is ", domainNumber + 1, ' colors.')
                print()
                break
        print()
    print('time = ', time.time() - startTime)


def runForwardChecking(constraintsWrapper, nodes, greedyColors, maxTime):
    print()
    startTime = time.time()
    allConstraints = constraintsWrapper.allConstraints[:]
    for domainNumber in range(greedyColors - 1, 0, -1):
        print('Trying to color in  ', domainNumber, ' colors ... ', end='')
        domains = {}
        for node in nodes:
            node.domains = [i + 1 for i in range(domainNumber)]
            node.initNeighborsColors()
            domains[node] = [i + 1 for i in range(domainNumber)]

        constraintsWrapper.allConstraints = allConstraints[:]
        csp = CSP(startTime, maxTime, nodes, constraintsWrapper, domains, [i + 1 for i in range(domainNumber)])
        if not csp.arcConsistency():
            print("No solution found with ", domainNumber, ' colors.')
            print()
            print("Minimum number of colors needed is ", domainNumber + 1, ' colors.')
            print()
            break

        solution = csp.forwardChecking()

        if solution is None:
            print("No solution found with ", domainNumber, ' colors.')
            print()
            print("Minimum number of colors needed is ", domainNumber + 1, ' colors.')
            print()
            break
        else:
            if checkSol(solution):
                print('Success !!')
                printSolution(solution)
            else:
                print("No solution found with ", domainNumber, ' colors.')
                print()
                print("Minimum colors needed is ", domainNumber + 1, ' colors.')
                print()
                break
        print()
    print('time = ', time.time() - startTime)


def runTabu(constraints, greedyColors, assignment, maxTime):
    startTime = time.time()
    fitnessType, neighborhoodType, args = getTabuArgs()
    for colorToDelete in range(greedyColors, 0, -1):
        deleteColor(assignment, [i + 1 for i in range(colorToDelete)])
        print('Trying to color in  ', colorToDelete - 1, ' colors ... ')
        domains = [i + 1 for i in range(colorToDelete - 1)]

        assignment, conflictsNum = tabuSearch(constraints, domains, args, assignment, fitnessType,
                                                      neighborhoodType, maxTime, startTime)

        if conflictsNum != 0:
            print("No solution found with ", colorToDelete - 1, ' colors.')
            print()
            print("Minimum number of colors needed is ", colorToDelete, ' colors.')
            print()
            break

        if checkSolutionConsistency(assignment, constraints):
            print('Success !!')
            printSolution(assignment)
        else:
            print("No solution found with ", colorToDelete - 1, ' colors.')
            print()
            print("Minimum number of colors needed is ", colorToDelete, ' colors.')
            print()
            break
        print()
    print('time = ', time.time() - startTime)


def runGA(greedyColors, nodes, maxTime):
    args = getGaArgs(len(nodes))
    startTime = time.time()
    for colors in range(greedyColors - 1, 0, -1):
        print('coloring in ', colors, ' colors')
        domain = [i + 1 for i in range(colors)]
        GA = GeneticAlgorithm(args, domain, nodes, startTime, maxTime)
        result, conflicts = GA.run()
        if conflicts != 0:
            print('No solution found with', colors, ' colors !!')
            print("Minimum number of colors needed is ", colors + 1, ' colors.')
            break
        print('Success !!')


def readGlobalArgs():
    file = open('INPUT\\GLOBAL_ARGS.txt', 'r')
    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxTime = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    path = str(arr[2])

    return maxTime, path


def getTabuArgs():
    file = open('INPUT\\TABU_ARGS.txt', 'r')  # input string

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxIter = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    localOptStop = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxTabu = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    numNeighbors = int(arr[2])

    fitnessType = None

    line = file.readline()
    arr = [num for num in line.split(' ')]
    fitness = int(arr[2])
    if fitness == 1:
        fitnessType = FitnessType.FEASIBLE

    line = file.readline()
    arr = [num for num in line.split(' ')]
    fitness = int(arr[2])
    if fitness == 1:
        fitnessType = FitnessType.OBJECTIVE

    line = file.readline()
    arr = [num for num in line.split(' ')]
    fitness = int(arr[2])
    if fitness == 1:
        fitnessType = FitnessType.HYBRID

    neighborhoodType = None

    line = file.readline()
    arr = [num for num in line.split(' ')]
    neighborhood = int(arr[2])
    if neighborhood == 1:
        neighborhoodType = NeighborhoodType.REGULAR

    line = file.readline()
    arr = [num for num in line.split(' ')]
    neighborhood = int(arr[2])
    if neighborhood == 1:
        neighborhoodType = NeighborhoodType.KEMPE

    return fitnessType, neighborhoodType, TabuArgs(maxIter, localOptStop, maxTabu, numNeighbors)


def getGaArgs(lenNodes):
    file = open('INPUT\\GA_ARGS.txt', 'r')  # input string

    line = file.readline()
    arr = [num for num in line.split(' ')]
    popsize = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxIter = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    eliteRate = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    mutationRate = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    tournamentK = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    minAge = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxAge = int(arr[2])

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

    args = GaArgs(popsize, maxIter, eliteRate, mutationRate,
                  tournamentK, minAge, maxAge, lenNodes, linearA, linearB, localOptMax,
                  cross, sel, mut)
    return args


if __name__ == '__main__':
    maxTime, path = readGlobalArgs()

    print('Enter the algorithm number want to run:')
    print('1 - Backtracking with backjumping')
    print('2 - ForwardChecking with AC-3')
    print('3 - Tabu Search')
    print('4 - Genetic Algorithm')

    algoNum = int(input())

    variables = readFile(path)
    if algoNum == 1:
        runBacktracking(variables['constraintsWrapper'], variables['nodes'], variables['greedyColors'], maxTime)
    elif algoNum == 2:
        runForwardChecking(variables['constraintsWrapper'], variables['nodes'], variables['greedyColors'], maxTime)
    elif algoNum == 3:
        runTabu(variables['constraintsWrapper'].constraintsByNode, variables['greedyColors'],
                variables['greedyAssignment'], maxTime)
    elif algoNum == 4:
        runGA(variables['greedyColors'], variables['nodes'], maxTime)
