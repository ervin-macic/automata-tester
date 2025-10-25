class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        """
        states: list of state names (strings)
        alphabet: list of allowed symbols (strings)
        start_state: string
        accept_states: list of accepting state names
        transitions: dict of the form {(state, symbol): next_state}
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = transitions

        self._validate()

    def _validate(self):
        # Check that start state and accept states are valid
        if self.start_state not in self.states:
            raise ValueError(f"Start state {self.start_state} not in states.")
        if not self.accept_states.issubset(self.states):
            raise ValueError("Accept states must be a subset of states.")

        # Check all transitions are valid
        for (state, symbol), next_state in self.transitions.items():
            if state not in self.states:
                raise ValueError(f"Invalid state in transition: {state}")
            if next_state not in self.states:
                raise ValueError(f"Invalid next state in transition: {next_state}")
            if symbol not in self.alphabet:
                raise ValueError(f"Invalid symbol in transition: {symbol}")

    def test_string(self, input_string):
        """Simulate DFA on a given input string."""
        current_state = self.start_state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, f"Invalid symbol '{symbol}' in input."
            key = (current_state, symbol)
            if key not in self.transitions:
                return False, f"No transition defined for ({current_state}, {symbol})."
            current_state = self.transitions[key]
        return (current_state in self.accept_states, f"Ended in {current_state}")

    def test_many(self, strings):
        """Test a list of strings and return a dict of results."""
        results = {}
        for s in strings:
            accepted, msg = self.test_string(s)
            results[s] = "ACCEPTED" if accepted else f"REJECTED ({msg})"
        return results