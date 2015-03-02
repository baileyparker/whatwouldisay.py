from random import random


class WeightedRandomizer:
    def __init__(self, items):
        self._total = 0
        self._weights = []

        for item, weight in items:
            self._total += weight
            self._weights.append((self._total, item))

    def random(self):
        r = random() * self._total

        for ceiling, item in self._weights:
            if ceiling > r:
                return item
