import numpy as np

class param:
    def __init__(self, p, size) -> None:
        self.code_distance = size
        self.errors_rate = np.array([p/3, p/3, p/3]) # X, Y, Z