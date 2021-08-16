from random import randint
from lab1.Particle import Particle


class PSO:

    def __init__(self, args):
        self.args = args
        self.particles = []
        self.globalBest = None
        self.globalBestFitness = float('inf')
        self.tsize = len(self.args.GA_TARGET)
        self.initParticles()
        self.C1 = 1
        self.C2 = 3
        self.W = 1

    def run(self):
        target = [ord(char) for char in self.args.GA_TARGET]
        found = False
        for t in range(self.args.GA_MAXITER):
            for particle in self.particles:
                particle.update(self.globalBest, self.C1, self.C2, self.W)
                fitness = self.calcFitness(particle.getString())
                particle.setFitness(fitness)
                self.updateGPBest(particle, fitness)
            self.sortByFitness()
            self.updateParameters(t, self.args.GA_MAXITER)
            if self.globalBestFitness == 0:
                print('the best is: ', self.globalBest, '(', self.globalBestFitness, ')')
                print('found.')
                found = True
                break
            print('the best is', self.globalBest, '(', self.globalBestFitness, ')')
        if not found:
            print('reached local optimum.')

    def updateParameters(self, t, N):   # update the PSO parameters
        self.W = 0.4 * ((t - N) / N ** 2) + 0.4
        self.C1 = -3 * (t / N) + 3.5
        self.C2 = 3 * (t / N) + 0.5

    def updateGPBest(self, particle, fitness):
        if particle.getBestFitness() > fitness:
            particle.setBestString(particle.getString())
            particle.setBestFitness(fitness)
        if self.globalBestFitness > fitness:
            self.globalBest = particle.getString()
            self.globalBestFitness = fitness

    def initParticles(self):
        for _ in range(self.args.GA_POPSIZE):
            randomPos = []
            randomVector = []
            for _ in range(self.tsize):
                x = randint(32, 126)
                randomPos.append(x)
                y = randint(32, 126)
                randomVector.append(y)
            # save the best string to be the GlobalBest
            if self.globalBest is None:
                self.globalBest = randomPos[0:]
            elif self.calcFitness(randomPos) < self.calcFitness(self.globalBest):
                self.globalBest = randomPos
            particle = Particle(randomPos, self.calcFitness(randomPos), randomVector)
            self.particles.append(particle)

    def calcFitness(self, particle):
        target = [ord(char) for char in self.args.GA_TARGET]
        fitness = 0
        for j in range(0, self.tsize):
            fitness += (abs(particle[j] - target[j]))
        return fitness

    def sortByFitness(self):
        self.particles.sort()
        self.globalBest = self.particles[0].getString()
        self.globalBestFitness = self.particles[0].getFitness()
