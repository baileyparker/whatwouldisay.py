from collections import deque

from StateDict import StateDict
from MarkovGenerator import MarkovGenerator


class MarkovBuilder:
    def __init__(self, order=2):
        if order < 1:
            raise ValueError('Markov chain order should be 1 or greater')

        self._order = order
        self._chain = StateDict()

    @property
    def order(self):
        return self._order

    def train(self, data):
        for state, future in self._get_markov_pairs(data):
            self._chain.add(state, future)

    def _get_markov_pairs(self, data):
        state = deque()
        future = None

        for item in data:
            if len(state) == self._order:
                state.popleft()

            if future:
                state.append(future)

            future = item

            yield tuple(state), future

    def build(self):
        return MarkovGenerator(self._chain.compile(), self._order)
