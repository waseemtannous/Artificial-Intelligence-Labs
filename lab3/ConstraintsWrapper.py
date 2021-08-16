class ConstraintsWrapper:
    def __init__(self, constraintsByNode: dict, allConstraints: list, leftConstraints: dict, rightConstraints: dict):
        self.constraintsByNode = constraintsByNode
        self.allConstraints = allConstraints
        self.leftConstraints = leftConstraints
        self.rightConstraints = rightConstraints
        self.constraintsDict = {}
        for constraint in self.allConstraints:
            self.constraintsDict[constraint] = True

    def addArcs(self, node):
        for constraint in self.rightConstraints[node]:
            if not self.constraintsDict[constraint]:
                self.allConstraints.append(constraint)
                self.constraintsDict[constraint] = True

