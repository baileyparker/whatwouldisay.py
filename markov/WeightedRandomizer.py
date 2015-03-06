from random import random


class WeightedRandomizer:
    """
    A utility class capable of producing weighted randoms in an efficient way.
    """
    def __init__(self, items):
        self._total = 0
        self._weights = []

        for item, weight in items:
            self._total += weight
            self._weights.append((self._total, item))

    def random(self):
        """
        Choose a random element (weighted) from the given randomizer's items.
        """
        r = random() * self._total

        for ceiling, item in self._weights:
            if ceiling > r:
                return item
