class NFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        """
        states: list of state names (strings)
        alphabet: list of allowed symbols (strings)
        start_state: string
        accept_states: list of accepting state names
        transitions: dict of the form {(state, symbol): set_of_next_states}
                      symbol can also be "" or "ε" for epsilon transitions
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = transitions

        self._validate()

    def _validate(self):
        if self.start_state not in self.states:
            raise ValueError(f"Start state {self.start_state} not in states.")
        if not self.accept_states.issubset(self.states):
            raise ValueError("Accept states must be a subset of states.")
        for (state, symbol), next_states in self.transitions.items():
            if state not in self.states:
                raise ValueError(f"Invalid state in transition: {state}")
            if not next_states.issubset(self.states):
                raise ValueError(f"Invalid next states in transition: {next_states}")
            if symbol not in self.alphabet and symbol not in {"", "ε"}:
                raise ValueError(f"Invalid symbol in transition: {symbol}")

    def _epsilon_closure(self, states):
        """Return the epsilon-closure (set of states reachable via ε) of the given states."""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for eps_symbol in ("", "ε"):
                if (state, eps_symbol) in self.transitions:
                    for next_state in self.transitions[(state, eps_symbol)]:
                        if next_state not in closure:
                            closure.add(next_state)
                            stack.append(next_state)
        return closure

    def test_string(self, input_string):
        """Simulate NFA on a given input string."""
        current_states = self._epsilon_closure({self.start_state})

        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, f"Invalid symbol '{symbol}' in input."

            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states |= self.transitions[(state, symbol)]

            current_states = self._epsilon_closure(next_states)

        accepted = any(state in self.accept_states for state in current_states)
        return accepted, f"Ended in states {current_states}"

    def test_many(self, strings):
        """Test a list of strings and return a dict of results."""
        results = {}
        for s in strings:
            accepted, msg = self.test_string(s)
            results[s] = "ACCEPTED" if accepted else f"REJECTED ({msg})"
        return results
