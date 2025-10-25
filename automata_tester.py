import time

from automathon import DFA, NFA
from automata_img_to_json import automata_img_to_json
from automata_utility import load_automata_from_json
from constants import test_strings

if __name__ == "__main__":
    file_name = "moc_ps1_p1_4.jpg"
    automata_type = "dfa"
    automata_img_to_json(file_name, automata_type)

    # Allow time for the json file update
    time.sleep(0.1)

    is_nfa = True if automata_type == "nfa" else False
    q, sigma, delta, initial_state, f = load_automata_from_json("temporary_automata_config.json", is_nfa)
    automata = NFA(q, sigma, delta, initial_state, f) if is_nfa else DFA(q, sigma, delta, initial_state, f)

    # Visualize the automata
    automata.view(
        file_name=f"visualizations/{file_name}",
        node_attr={'fontsize': '20'},
        edge_attr={'fontsize': '20pt'}
    )

    print("\nAutomata Test Results:")
    for s in test_strings:
        if automata.accept(s):
            if s == "":
                print("ε")
            else:
                print(s)
