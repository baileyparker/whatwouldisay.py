from collections import deque

from StateDict import StateDict
from MarkovGenerator import MarkovGenerator


class MarkovBuilder:
    """
    A Builder that can train a markov model on data and then create a
    `MarkovGenerator` to generate chains from the model.

    The order of the model is actually the max order, because the builder
    uses a sliding window view of the input data to build the chains. For the
    first (order - 1) state/future pairs the state, the state is only as
    long as the number of tokens already encountered. Thus, an 3rd order model
    is also implicitly a 2nd, 1st, and 0th order (for picking the first token).
    """
    def __init__(self, order=2):
        if order < 1:
            raise ValueError('Markov chain order should be 1 or greater')

        self._order = order
        self._chain = StateDict()

    @property
    def order(self):
        """
        Return the (max) order of the model being built.
        """
        return self._order

    def train(self, data):
        """
        Train the model on input data. This data is assumed to be contiguous.
        """
        for state, future in self._get_markov_pairs(data):
            self._chain.add(state, future)

    def _get_markov_pairs(self, data):
        """
        Generates a "sliding window" state and future pair for each token in
        the data.
        """
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
        """
        Builds a `MarkovGenerator` from the currently trained chain.
        """
        return MarkovGenerator(self._chain.compile(), self._order)
