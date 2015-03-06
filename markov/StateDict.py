from collections import defaultdict, Counter

from CompiledStateDict import CompiledStateDict


class StateDict:
    """
    A state to future mapping representing a n-th order Markov chain.

    Used as an intermediary in the building process, a StateDict object
    should be compiled via `StateDict.compile()` before use.
    """
    def __init__(self):
        self._states = defaultdict(Counter)

    def __len__(self):
        """
        Calculate the number of (state -> future) contained by the dict.
        """
        return len(self._states)

    def add(self, state, future):
        """
        Add a state and future to the chain's probabilities.

        Iteratively adds for the state sans its leftmost token.
        ex. add((a, b), c) adds (a, b) -> c, (b) -> c, () -> c
        """
        for state_chunk in self._shrink_right(state):
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
        return CompiledStateDict(self._states)
