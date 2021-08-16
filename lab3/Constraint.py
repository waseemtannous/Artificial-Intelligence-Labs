class Constraint:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def isSatisfied(self, assignment: dict):
        if self.node1 not in assignment or self.node2 not in assignment:
            return True
        return assignment[self.node1] != assignment[self.node2]
