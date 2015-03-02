from collections import deque


class MarkovGenerator:
    def __init__(self, chain, order):
        self._chain = chain
        self._order = order

    @property
    def order(self):
        return self._order

    def generate(self, length):
        state = deque()

        for _ in range(length):
            current = self._chain[tuple(state)].random()

            yield current

            if len(state) == self._order:
                state.popleft()

            state.append(current)
