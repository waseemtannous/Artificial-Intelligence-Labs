from lab3.Node import *
from lab3.ConstraintsWrapper import *
from time import time


class CSP:
    def __init__(self, startTime, maxTime, nodes: list, constraintsWrapper: ConstraintsWrapper, domains: dict,
                 domainsArr: list):
        self.startTime = startTime
        self.maxTime = maxTime
        self.nodes = nodes
        self.constraintsWrapper = constraintsWrapper
        self.domains = domains
        self.domainsArr = domainsArr
        self.coloredNodes = []
        self.assignment = {}
        self.startNode = None
        self.colored = 0
        self.unassigned = []
        self.conflictNode = None
        self.conflictSet = {}
        for node in nodes:
            self.conflictSet[node] = []

    def checkTime(self):
        return time() - self.startTime < self.maxTime

    def isConsistent(self, node, assignment):
        for constraint in self.constraintsWrapper.constraintsByNode[node]:
            if not constraint.isSatisfied(assignment):
                return False
        return True

    def forwardChecking(self, time=0, assignment=None, domains=None):
        if assignment is None:
            assignment = {}
        if domains is None:
            domains = self.domains
        if len(assignment) == len(self.nodes):
            return assignment
        if not self.checkTime():
            return None

        unassigned = [node for node in self.nodes if node not in assignment]

        node = self.getNode(unassigned, domains)
        node.time = time
        domains = self.LCV(node, assignment, domains)
        for value in domains[node]:
            toBreak = False
            localAssignment = {key: value for key, value in assignment.items()}  # deep copy
            localAssignment[node] = value
            localDomains = {key: value[:] for key, value in domains.items()}  # deep copy
            if self.isConsistent(node, localAssignment):
                if len(localAssignment) == len(self.nodes):
                    return localAssignment
                neighbors = node.neighbors
                for neighbor in neighbors:
                    if neighbor not in assignment:
                        if value in localDomains[neighbor]:
                            localDomains[neighbor].remove(value)
                            if len(localDomains[neighbor]) == 0:
                                toBreak = True
                                break
                if toBreak:
                    continue
                result = self.forwardChecking(time + 1, localAssignment, localDomains)
                if result is not None:
                    return result
        return None

    def backtracking(self, time=0, assignment=None, domains=None):
        if assignment is None:
            assignment = {}
        if domains is None:
            domains = self.domains
        if len(assignment) == len(self.nodes):
            return assignment
        if not self.checkTime():
            return None

        unassigned = [node for node in self.nodes if node not in assignment]

        node = self.getNode(unassigned, domains)
        node.time = time
        self.conflictNode = None
        self.LCV(node, assignment, domains)
        for value in domains[node]:
            localAssignment = {key: value for key, value in assignment.items()}  # deep copy
            localAssignment[node] = value
            localDomains = {key: value[:] for key, value in domains.items()}  # deep copy
            if self.isConsistent(node, localAssignment):
                localDomains[node].remove(value)
                for neighbor in node.neighbors:
                    if value in localDomains[neighbor]:
                        localDomains[neighbor].remove(value)

                self.updateConflictSet(node)
                result = self.backtracking(time + 1, localAssignment, localDomains)
                if result is not None:
                    return result

        self.updateAllConflictSets(node)
        if self.conflictNode is not None:
            result = self.backtracking(time + 1, assignment, domains)
            if result is not None:
                return result
        return None

    def updateAllConflictSets(self, node):
        if len(self.conflictSet[node]) > 0:
            self.conflictNode = self.conflictSet[node][-1]
            for i in range(len(self.conflictSet[node]), -1, -1):
                nodeI = self.conflictSet[node][i]
                for j in range(i - 1, -1 - 1):
                    nodeJ = self.conflictSet[node][j]
                    if nodeJ not in self.conflictSet[nodeI]:
                        self.conflictSet[nodeI].append(nodeJ)
                sorted(self.conflictSet[nodeI], key=attrgetter('time'))
            self.conflictSet[node] = []

    def updateConflictSet(self, node):
        for neighbor in node.neighbors:
            if neighbor in self.assignment:
                if neighbor not in self.conflictSet[node]:
                    self.conflictSet[node].append(neighbor)
        sorted(self.conflictSet[node], key=attrgetter('time'))

    def getNode(self, unassigned, domains):
        if self.conflictNode is not None:
            return self.conflictNode
        return self.MRV(unassigned, domains)

    def MRV(self, unassigned, domains):  # choose node with minimum domains left
        minLen = float('inf')
        retNode = None
        for node in unassigned:
            length = len(domains[node])
            # check singleton
            if length == 1:
                return node
            if length < minLen:
                minLen = length
                retNode = node
            elif length == minLen:  # solves equality
                if len(self.constraintsWrapper.constraintsByNode[node]) > \
                        len(self.constraintsWrapper.constraintsByNode[retNode]):
                    minLen = length
                    retNode = node
        return retNode

    def LCV(self, node, assignment, domains):
        neighbors = node.neighbors
        futureOptions = {}
        for value in domains[node]:
            counter = 0
            assignment[node] = value
            # if it is not consistent
            if not self.isConsistent(node, assignment):
                futureOptions[value] = 0
                continue
            for neighbor in neighbors:
                if neighbor not in assignment:  # if isn't colored
                    for tempVal in domains[neighbor]:
                        if tempVal != value:
                            counter += 1
                if counter == 0:
                    break
            futureOptions[value] = counter
        assignment.pop(node, None)
        sorted(futureOptions.items(), key=lambda kv: (kv[1], kv[0]))
        d = [k for k, v in sorted(futureOptions.items(), key=lambda item: item[1])]
        d.reverse()
        domains[node] = d
        return domains

    def checkNodeWithNeighbors(self, node, value, assignment):
        for neighbor in node.neighbors:
            if not assignment.get(neighbor, False):
                continue
            if value == assignment[neighbor]:
                return False
        return True

    def arcConsistency(self):
        while len(self.constraintsWrapper.allConstraints) != 0:
            constraint = self.constraintsWrapper.allConstraints.pop(0)
            self.constraintsWrapper.constraintsDict[constraint] = False
            firstNode = constraint.node1
            secondNode = constraint.node2

            firstDomains = self.domains[firstNode]
            secondDomains = self.domains[secondNode]

            addOppositeArcs = False
            removeValues = []
            noSatisfactionFound = True
            for val1 in firstDomains:
                found = False
                for val2 in secondDomains:
                    if val1 != val2:
                        found = True
                        noSatisfactionFound = False
                if not found:
                    removeValues.append(val1)
            if noSatisfactionFound:
                return False
            for val in removeValues:
                self.domains[firstNode].remove(val)
                addOppositeArcs = True
            if addOppositeArcs:
                self.constraintsWrapper.addArcs(firstNode)
        return True
