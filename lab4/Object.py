class Object:
    def __init__(self, name, value: int, weight: int):
        self.name = name
        self.value = value
        self.weight = weight
        self.density = 0
        if weight == 0:
            self.density = float('inf')
        else:
            self.density = float(value / weight)
