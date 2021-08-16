from lab2.City import *
from lab2.CVRP import *
from lab2.TabuSearch import *
from lab2.SimulatedAnnealing import *
from lab2.GeneticAlgorithm import *
from lab2.Variables import *
from lab2.ACO import *
from math import sqrt
from tkinter import *
from tkinter.ttk import Combobox


def getInput(probNum):
    file = open('INPUT\\' + str(probNum) + '.txt', 'r')  # input string
    for _ in range(3):
        file.readline()

    dimensionLine = file.readline()
    arr = [num for num in dimensionLine.split(' ')]
    dimension = int(arr[2])

    file.readline()

    capacityLine = file.readline()
    arr = [num for num in capacityLine.split(' ')]
    capacity = int(arr[2])

    file.readline()

    cityLine = file.readline()
    arr = [num for num in cityLine.split(' ')]
    depot = City(int(arr[0]), int(arr[1]), int(arr[2]))

    cities = []
    for _ in range(dimension - 1):
        cityLine = file.readline()
        arr = [num for num in cityLine.split(' ')]
        city = City(int(arr[0]) - 1, int(arr[1]), int(arr[2]))
        cities.append(city)

    file.readline()
    file.readline()

    for i in range(dimension - 1):
        demandLine = file.readline()
        arr = [num for num in demandLine.split(' ')]
        cities[i].setDemand(int(arr[1]))

    cities.insert(0, depot)

    distanceMat = calcDistanceMatrix(cities)
    cities.pop(0)

    problem = CVRP(distanceMat, depot, cities, capacity, len(cities))

    return problem


def calcDistanceMatrix(cities):
    array = []
    numOfCities = len(cities)
    for i in range(numOfCities):
        arr = []
        for j in range(numOfCities):
            arr.append(distance(cities[i], cities[j]))
        array.append(arr)
    return array


def distance(city1, city2):
    x = city1.x - city2.x
    dx = x * x

    y = city1.y - city2.y
    dy = y * y

    return sqrt(dx + dy)


def getTabuArgs(ArgsPath):
    file = open(ArgsPath, 'r')  # input string

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

    return TabuArgs(maxIter, localOptStop, maxTabu, numNeighbors)


def getSimuArgs(argsPath):
    file = open(argsPath, 'r')  # input string

    line = file.readline()
    arr = [num for num in line.split(' ')]
    temperature = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    alpha = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxIter = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    localOptStop = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    numNeighbors = int(arr[2])

    return SimuArgs(temperature, alpha, maxIter, localOptStop, numNeighbors)


def getACOArgs(argsPath):
    file = open(argsPath, 'r')  # input string

    line = file.readline()
    arr = [num for num in line.split(' ')]
    maxIter = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    localOptStop = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    a = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    b = float(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    q = int(arr[2])

    line = file.readline()
    arr = [num for num in line.split(' ')]
    p = float(arr[2])

    return ACOArgs(maxIter, localOptStop, a, b, q, p)


def runAlgorithm(argsPath, argsFunction, algoFunction, path):
    args = argsFunction(argsPath)
    problem = getInput(path)
    algoFunction(problem, args)
    printSolution(problem)


def printSolution(problem):
    problem.printSolution()


def getUiInput():
    popsize = int(ENTRIES[0].get())
    maxIter = int(ENTRIES[1].get())
    eliteRate = float(ENTRIES[2].get())
    mutationRate = float(ENTRIES[3].get())
    tournamentK = int(ENTRIES[4].get())
    minAge = int(ENTRIES[5].get())
    maxAge = int(ENTRIES[6].get())
    linearA = int(ENTRIES[7].get())
    linearB = int(ENTRIES[8].get())
    localOptMax = int(ENTRIES[9].get())
    probNum = int(ENTRIES[10].get())
    crossover = str(ENTRIES[11].get())
    selection = str(ENTRIES[12].get())
    mutation = str(ENTRIES[13].get())

    cross, sel, mut = None, None, None

    if crossover == 'PMX':
        cross = CrossoverType.PMX
    else:
        cross = CrossoverType.OX

    if selection == 'RWS':
        sel = SelectionType.RWS
    elif selection == 'SUS':
        sel = SelectionType.SUS
    else:
        sel = SelectionType.TOURNAMENT

    if mutation == 'Exchange':
        mut = MutationType.EXCHANGE
    else:
        mut = MutationType.SIMPLE_INVERSION

    problem = getInput(probNum)

    args = GaArgs(popsize, maxIter, eliteRate, mutationRate,
                  tournamentK, minAge, maxAge, problem.size, linearA, linearB, localOptMax,
                  cross, sel, mut)
    return args, problem


def GArun():
    args, problem = getUiInput()
    GA = GeneticAlgorithm(args, problem)
    GA.run()
    printSolution(problem)


def gaUI():
    root = Tk()

    root.title("Ai Lab 2 - Genetic Algorithm")
    root.configure(background='#2b2b2b')
    root.geometry("800x700")  # width X height
    root.resizable(False, False)

    Label(root, text="population size", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=0,
                                                                                                            padx=10,
                                                                                                            pady=10)
    Label(root, text="max iterations", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=1,
                                                                                                           padx=10,
                                                                                                           pady=10)
    Label(root, text="elite rate", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=2, padx=10,
                                                                                                       pady=10)
    Label(root, text="mutation rate", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=3,
                                                                                                          padx=10,
                                                                                                          pady=10)
    Label(root, text="K variable (tournament selection)", bg='#3c3f41', fg='#a9b7c6', bd=0,
          font=("JetBrains Mono", 18)).grid(row=4, padx=10, pady=10)
    Label(root, text="min age", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=5, padx=10,
                                                                                                    pady=10)
    Label(root, text="max age", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=6, padx=10,
                                                                                                    pady=10)

    Label(root, text="linear scaling A", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=7,
                                                                                                             padx=10,
                                                                                                             pady=10)
    Label(root, text="linear scaling B", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=8,
                                                                                                             padx=10,
                                                                                                             pady=10)
    Label(root, text="local optimum iterations limit", bg='#3c3f41', fg='#a9b7c6', bd=0,
          font=("JetBrains Mono", 18)).grid(row=9, padx=10, pady=10)

    Label(root, text="problem", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=10, padx=10, pady=10)

    Label(root, text="crossover Type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=11, padx=10, pady=10)

    Label(root, text="selection Type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=12, padx=10, pady=10)

    Label(root, text="mutation Type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=13, padx=10, pady=10)

    e1 = Entry(root)
    e2 = Entry(root)
    e3 = Entry(root)
    e4 = Entry(root)
    e5 = Entry(root)
    e6 = Entry(root)
    e7 = Entry(root)
    e8 = Entry(root)
    e9 = Entry(root)
    e10 = Entry(root)
    e11 = Entry(root)

    ENTRIES.append(e1)
    ENTRIES.append(e2)
    ENTRIES.append(e3)
    ENTRIES.append(e4)
    ENTRIES.append(e5)
    ENTRIES.append(e6)
    ENTRIES.append(e7)
    ENTRIES.append(e8)
    ENTRIES.append(e9)
    ENTRIES.append(e10)
    ENTRIES.append(e11)

    e1.insert(END, '2048')  # pop size
    e2.insert(END, '16384')  # max iter
    e3.insert(END, '0.1')  # elite rate
    e4.insert(END, '0.5')  # mutation rate
    e5.insert(END, '10')  # tournament k
    e6.insert(END, '2')  # min age
    e7.insert(END, '30')  # max age
    e8.insert(END, '1')  # linear scaling A
    e9.insert(END, '10')  # linear scaling B
    e10.insert(END, '30')  # local opt stop
    e11.insert(END, '1')  # problem number

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    e6.grid(row=5, column=1)
    e7.grid(row=6, column=1)
    e8.grid(row=7, column=1)
    e9.grid(row=8, column=1)
    e10.grid(row=9, column=1)
    e11.grid(row=10, column=1)

    choices = ['PMX', 'OX']
    crossoverChoicebox = Combobox(root, values=choices)
    crossoverChoicebox.current(0)
    crossoverChoicebox.grid(row=11, column=1)

    ENTRIES.append(crossoverChoicebox)

    choices = ['RWS', 'SUS', 'Tournament']
    selectionChoicebox = Combobox(root, values=choices)
    selectionChoicebox.current(1)
    selectionChoicebox.grid(row=12, column=1)

    ENTRIES.append(selectionChoicebox)

    choices = ['Exchange', 'Simple Inversion']
    mutationChoicebox = Combobox(root, values=choices)
    mutationChoicebox.current(0)
    mutationChoicebox.grid(row=13, column=1)

    ENTRIES.append(mutationChoicebox)

    Button(root, text="Run Genetic Algorithm", command=lambda: GArun(), bg='#3c3f41', fg='#a9b7c6', bd=0,
           font=("JetBrains Mono", 18)).grid(row=4, column=2, padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    print('Enter the algorithm number want to run:')
    print('1 - Tabu Search')
    print('2 - Simulated Annealing')
    print('3 - ACO')
    print('4 - Genetic Algorithm')
    algoNum = int(input())
    if algoNum == 4:
        gaUI()
    else:
        print('Enter the problem number you want to run:')
        problemNum = str(input())
        algoFunction = None
        argsFunction = None
        argsPath = None
        if algoNum == 1:
            argsPath = 'INPUT\\TABU_ARGS.txt'
            argsFunction = getTabuArgs
            algoFunction = tabuSearch
        elif algoNum == 2:
            argsPath = 'INPUT\\SIMU_ARGS.txt'
            argsFunction = getSimuArgs
            algoFunction = simulatedAnnealing
        elif algoNum == 3:
            argsPath = 'INPUT\\ACO_ARGS.txt'
            argsFunction = getACOArgs
            algoFunction = ACO
        runAlgorithm(argsPath, argsFunction, algoFunction, problemNum)
    input()
