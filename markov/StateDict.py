from collections import deque, Counter

from WeightedRandomizer import WeightedRandomizer


class StateDict:
    def __init__(self, states=None):
        self._states = states if states else {}

    def __getitem__(self, state):
        state = deque(state)

        while True:
            try:
                return self._states[tuple(state)]
            except KeyError:
                state.popleft()

    def add(self, state, future):
        for state_chunk in self._shrink_right(state):
            if state_chunk not in self._states:
                self._states[state_chunk] = Counter()

            self._states[state_chunk][future] += 1

    def _shrink_right(self, state):
        for l in range(-len(state), 1):
            yield tuple(state[l:])

    def compile(self):
        return StateDict({s: WeightedRandomizer(f.most_common())
                         for s, f in self._states.iteritems()})
