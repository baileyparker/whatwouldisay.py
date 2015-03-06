from collections import deque, Counter

from WeightedRandomizer import WeightedRandomizer


class StateDict:
    """
    A state to future mapping representing a n-th order Markov chain.
    """
    def __init__(self, states=None):
        self._states = states if states else {}

    def __getitem__(self, state):
        """
        Predict the future element for a given state.

        Collapses the given state until it can find one for which probable
        futures exist (in the event a state never present in the training data
        is encountered).
        """
        state = deque(state)

        # Not infinite because there are always predictions for the empty state
        while True:
            try:
                return self._states[tuple(state)]
            except KeyError:
                state.popleft()

    def add(self, state, future):
        """
        Add a state and future to the chain's probabilities.

        Iteratively adds for the state sans its leftmost token.
        ex. add((a, b), c) adds (a, b) -> c, (b) -> c, () -> c
        """
        for state_chunk in self._shrink_right(state):
            if state_chunk not in self._states:
                self._states[state_chunk] = Counter()

            self._states[state_chunk][future] += 1

    def _shrink_right(self, state):
        """
        Shrink a state towards the right, until it is empty.
        """
        for l in range(-len(state), 1):
            yield tuple(state[l:])

    def compile(self):
        """
        Compile the StateDict into one that returns randomizers (for choosing
        a weighted random future given a state).
        """
        return StateDict({s: WeightedRandomizer(f.most_common())
                         for s, f in self._states.iteritems()})
