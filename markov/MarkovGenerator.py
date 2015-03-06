from collections import deque


class MarkovGenerator:
    """
    A generator of tokens that uses a previously trained Markov model.
    """
    def __init__(self, chain, order):
        self._chain = chain
        self._order = order

    @property
    def order(self):
        """
        Return the (max) order of the chain used by the generator.
        """
        return self._order

    def generate(self, length):
        """
        Generate a list of tokens of a given length using the
        previously-trained Markov chain.
        """
        state = deque()

        for _ in range(length):
            current = self._chain[tuple(state)].random()

            yield current

            if len(state) == self._order:
                state.popleft()

            state.append(current)
