from tkinter.ttk import Combobox

from lab1.GeneticAlgorithm import *
from lab1.NQueens import *
from lab1.Knapsack import *
from lab1.KnapsackProblem import *
from lab1.MinimalConflicts import *
import time
from lab1.Functions import *
from lab1.PSO import *
from tkinter import *
from lab1.Variables import *


def KNAPSACKrun():
    args = getInput()

    capacity, weights, profits, optimalSolution = knapsackReadInput(args.KNAPSACK_NUM)

    knapsackProblem = KnapsackProblem(capacity, weights, profits, optimalSolution)
    KS = Knapsack(knapsackProblem, args)
    run(KS)


def knapsackReadInput(problemNumber):
    capacity, weights, profits, optimalSolution = None, None, None, None

    probNum = str(problemNumber) + '\\'
    string = 'S:\\onedrive\\sync\\AILab\\lab1\\knapsackProblems\\problem'

    with open(string + probNum + 'Capacity.txt', 'r') as f:
        capacity = int(f.readline())

    with open(string + probNum + 'Weights.txt', 'r') as f:
        weights = [int(line) for line in f]

    with open(string + probNum + 'Profits.txt', 'r') as f:
        profits = [int(line) for line in f]

    with open(string + probNum + 'OptimalSolution.txt', 'r') as f:
        optimalSolution = [int(line) for line in f]

    return capacity, weights, profits, optimalSolution


def MinimalConflictsRun():
    args = getInput()
    minimalConflicts = MinimalConflicts(args)
    minimalConflicts.run()


def PSOrun():
    args = getInput()
    pso = PSO(args)
    pso.run()


def run(problem):
    startTime = time.time()
    problem.initPopulation()

    repeat = 0
    bestFitness = float('inf')

    found = False

    for _ in range(problem.args.GA_MAXITER):
        iterTime = time.time()
        problem.calcFitness()
        sortByFitness(problem)
        printBest(problem)
        calcAvgSd(problem)

        # this checks if we have reached a local optimum or found the goal
        if repeat == problem.args.LOCAL_STOP_ITER or problem.population[0].getFitness() == 0:
            print('Generation time: ', time.time() - iterTime)
            print()
            print('found.')
            found = True
            break

        genBestFit = problem.population[0].getFitness()

        if bestFitness == genBestFit:
            repeat += 1
        elif genBestFit < bestFitness:
            bestFitness = genBestFit
            repeat = 1

        try:
            problem.mate()
        except:
            print('Generation time: ', time.time() - iterTime)
            break
        swap(problem)
        aging(problem)
        print('Generation time: ', time.time() - iterTime)
        print()
    print('Time elapsed: ', time.time() - startTime)
    if not found:
        print('reached local optimum.')


def GArun():
    args = getInput()
    GA = GeneticAlgorithm(args)
    run(GA)


def NQUEENSrun():
    args = getInput()
    NQUEENs = NQueens(args)
    run(NQUEENs)


def getInput():
    popsize = int(ENTRIES[0].get())
    maxIter = int(ENTRIES[1].get())
    eliteRate = float(ENTRIES[2].get())
    mutationRate = float(ENTRIES[3].get())
    targetString = str(ENTRIES[4].get())
    tournamentK = int(ENTRIES[5].get())
    minAge = int(ENTRIES[6].get())
    maxAge = int(ENTRIES[7].get())
    N = int(ENTRIES[8].get())
    linearA = int(ENTRIES[9].get())
    linearB = int(ENTRIES[10].get())
    localOptMax = int(ENTRIES[11].get())
    knapsackProblem = int(ENTRIES[12].get())
    crossover = str(ENTRIES[13].get())
    selection = str(ENTRIES[14].get())
    mutation = str(ENTRIES[15].get())
    fitness = str(ENTRIES[16].get())

    cross, sel, mut, fit = None, None, None, None

    if crossover == 'One Point':
        cross = CrossoverType.ONE_POINT
    elif crossover == 'Two Point':
        cross = CrossoverType.TWO_POINT
    elif crossover == 'Uniform':
        cross = CrossoverType.UNIFORM
    elif crossover == 'PMX':
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

    if fitness == 'Character Distance':
        fit = FitnessType.CHARACTER_DISTANCE
    else:
        fit = FitnessType.BULLSEYE

    args = Arguments(popsize, maxIter, eliteRate, mutationRate, targetString,
                     tournamentK, minAge, maxAge, N, linearA, linearB, localOptMax,
                     knapsackProblem, cross, sel, mut, fit)
    return args


if __name__ == '__main__':
    root = Tk()

    root.title("Ai Lab 1")
    root.configure(background='#2b2b2b')
    root.geometry("800x900")  # width X height
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
    Label(root, text="target string", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=4,
                                                                                                          padx=10,
                                                                                                          pady=10)
    Label(root, text="K variable (tournament selection)", bg='#3c3f41', fg='#a9b7c6', bd=0,
          font=("JetBrains Mono", 18)).grid(row=5, padx=10, pady=10)
    Label(root, text="min age", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=6, padx=10,
                                                                                                    pady=10)
    Label(root, text="max age", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=7, padx=10,
                                                                                                    pady=10)
    Label(root, text="N for Nqueens", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=8,
                                                                                                          padx=10,
                                                                                                          pady=10)
    Label(root, text="linear scaling A", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=9,
                                                                                                             padx=10,
                                                                                                             pady=10)
    Label(root, text="linear scaling B", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(row=10,
                                                                                                             padx=10,
                                                                                                             pady=10)
    Label(root, text="local optimum iterations limit", bg='#3c3f41', fg='#a9b7c6', bd=0,
          font=("JetBrains Mono", 18)).grid(row=11, padx=10, pady=10)
    Label(root, text="knapsack problem number", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=12, padx=10, pady=10)

    Label(root, text="crossover Type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=13, padx=10, pady=10)

    Label(root, text="selection Type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=14, padx=10, pady=10)

    Label(root, text="mutation Type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=15, padx=10, pady=10)

    Label(root, text="fitness type", bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=16, padx=10, pady=10)

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
    e12 = Entry(root)
    e13 = Entry(root)

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
    ENTRIES.append(e12)
    ENTRIES.append(e13)

    e1.insert(END, '2048')
    e2.insert(END, '16384')
    e3.insert(END, '0.1')
    e4.insert(END, '0.5')
    e5.insert(END, 'Hello World!')
    e6.insert(END, '10')
    e7.insert(END, '2')
    e8.insert(END, '30')
    e9.insert(END, '12')
    e10.insert(END, '1')
    e11.insert(END, '10')
    e12.insert(END, '15')
    e13.insert(END, '1')

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
    e12.grid(row=11, column=1)
    e13.grid(row=12, column=1)

    choices = ['One Point', 'Two Point', 'Uniform', 'PMX', 'OX']
    crossoverChoicebox = Combobox(root, values=choices)
    crossoverChoicebox.current(1)
    crossoverChoicebox.grid(row=13, column=1)

    ENTRIES.append(crossoverChoicebox)

    choices = ['RWS', 'SUS', 'Tournament']
    selectionChoicebox = Combobox(root, values=choices)
    selectionChoicebox.current(1)
    selectionChoicebox.grid(row=14, column=1)

    ENTRIES.append(selectionChoicebox)

    choices = ['Exchange', 'Simple Inversion']
    mutationChoicebox = Combobox(root, values=choices)
    mutationChoicebox.current(0)
    mutationChoicebox.grid(row=15, column=1)

    ENTRIES.append(mutationChoicebox)

    choices = ['Character Distance', 'Bullseye']
    fitnessChoicebox = Combobox(root, values=choices)
    fitnessChoicebox.current(1)
    fitnessChoicebox.grid(row=16, column=1)

    ENTRIES.append(fitnessChoicebox)

    Button(root, text="Run Genetic Algorithm", command=GArun, bg='#3c3f41', fg='#a9b7c6', bd=0,
           font=("JetBrains Mono", 18)).grid(row=4, column=2, padx=10, pady=10)
    Button(root, text="Run N-Queens", command=NQUEENSrun, bg='#3c3f41', fg='#a9b7c6', bd=0,
           font=("JetBrains Mono", 18)).grid(row=5, padx=10, column=2, pady=10)
    Button(root, text="Run Knapsack", command=KNAPSACKrun, bg='#3c3f41', fg='#a9b7c6', bd=0,
           font=("JetBrains Mono", 18)).grid(row=6, padx=10, column=2, pady=10)
    Button(root, text="Run Minimal Conflicts", command=MinimalConflictsRun, bg='#3c3f41', fg='#a9b7c6', bd=0,
           font=("JetBrains Mono", 18)).grid(row=7, column=2, padx=10, pady=10)
    Button(root, text="Run PSO", command=PSOrun, bg='#3c3f41', fg='#a9b7c6', bd=0, font=("JetBrains Mono", 18)).grid(
        row=8, column=2, padx=10, pady=10)

    root.mainloop()
