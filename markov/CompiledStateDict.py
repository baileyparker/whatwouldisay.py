from collections import deque

from WeightedRandomizer import WeightedRandomizer


class CompiledStateDict:
    """
    A compiled state to future mapping representing a n-th order Markov chain.
    """
    def __init__(self, states):
        self._states = {s: WeightedRandomizer(f.most_common())
                        for s, f in states.iteritems()}

    def __getitem__(self, state):
        """
        Get a predictor for the future element given a state.

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
