import json

def load_automata_from_json(path, nfa=False):
    """
    Load a DFA or NFA definition from a JSON file and return:
        q, sigma, delta, initial_state, f

    Args:
        path (str): Path to the JSON automaton definition.
        nfa (bool): If True, interpret transitions as NFA-style
                    (delta[state][symbol] = set[str]).
                    If False, interpret as DFA-style
                    (delta[state][symbol] = str).

    JSON format expected:
    {
        "states": ["q1", "q2"],
        "alphabet": ["0", "1"],
        "start_state": "q1",
        "accept_states": ["q1"],
        "transitions": {
            "q1": {"0": ["q2"], "1": ["q1"]},
            "q2": {"0": ["q1"], "1": ["q2"]}
        }
    }
    """
    with open(path, "r") as f:
        data = json.load(f)

    q = set(data["states"])
    sigma = set(data["alphabet"])
    initial_state = data["start_state"]
    f = set(data["accept_states"])

    delta = {}

    for state, transitions in data["transitions"].items():
        delta[state] = {}
        for symbol, next_state in transitions.items():

            # --- Handle NFA (sets of next states)
            if nfa:
                if isinstance(next_state, list):
                    delta[state][symbol] = set(next_state)
                else:
                    delta[state][symbol] = {next_state}

            # --- Handle DFA (single next state)
            else:
                if isinstance(next_state, list):
                    if len(next_state) != 1:
                        raise ValueError(
                            f"Non-deterministic transition found in DFA: δ({state}, {symbol}) = {next_state}"
                        )
                    next_state = next_state[0]
                delta[state][symbol] = next_state

    return q, sigma, delta, initial_state, f



