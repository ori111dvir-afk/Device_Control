class Controller:
    def __init__(self, threshold: float = 50.0):
        self.threshold = threshold

    def check(self, value: float) -> bool:
        return value > self.threshold
