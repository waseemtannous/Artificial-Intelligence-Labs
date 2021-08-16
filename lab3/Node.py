from operator import attrgetter


class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.conflictSet = []
        self.conflictHash = {}
        self.time = 0
        self.color = None
        self.domains = []
        self.neighborColors = {}
        self.see = 0

    def addNeighbor(self, node):
        self.neighbors.append(node)

    def initNeighborsColors(self):
        for num in self.domains:
            self.neighborColors[num] = 0

    def updateNeighborsColors(self, value, flag):
        # if flag == -1:
        #     self.domains.remove(value)
        for neighbor in self.neighbors:
            if flag == 1:
                if value in neighbor.domains:
                    neighbor.domains.remove(value)
            if neighbor.neighborColors[value] == 0 and flag == -1:
                continue
            neighbor.neighborColors[value] += flag
            if neighbor.neighborColors[value] == 0:
                neighbor.domains.append(value)

    def updateConflictSet(self, conflictSet, index):
        for i in range(index):
            if not self.conflictHash.get(conflictSet[i], False):
                self.conflictSet.append(conflictSet[i])
        sorted(self.conflictSet, key=attrgetter('time'))
