class Stadium:
    def __init__(self, name: str, location: str, capacity: int, dimensions: dict[float, dict[str, float]]):
        self.name = name
        self.location = location
        self.capacity = capacity
        self.dimensions = dimensions