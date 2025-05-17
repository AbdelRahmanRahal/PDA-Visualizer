from pda.PDA import PDA

def main():
	# Example PDA that accepts strings with equal numbers of a's and b's
    states = {'q0', 'q1', 'q2'}
    input_alphabet = {'a', 'b'}
    stack_alphabet = {'A', 'B', '$'}
    transitions = {
        ('q0', 'a', '$'): [('q0', 'A$')],
        ('q0', 'a', 'A'): [('q0', 'AA')],
        ('q0', 'a', 'B'): [('q0', 'ε')],  # Pop B when seeing a
        ('q0', 'b', '$'): [('q0', 'B$')],
        ('q0', 'b', 'B'): [('q0', 'BB')],
        ('q0', 'b', 'A'): [('q0', 'ε')],  # Pop A when seeing b
        ('q0', 'ε', '$'): [('q1', '$')]   # Transition to accept state
    }
    initial_state = 'q0'
    initial_stack_symbol = '$'
    final_states = {'q1'}

    pda = PDA(states, input_alphabet, stack_alphabet, transitions,
              initial_state, initial_stack_symbol, final_states)

    # Test the PDA
    test_strings = ['ab', 'aabb', 'aaabbb', 'aab', 'bba']
    for test in test_strings:
        result = pda.process_input(test)
        print(f"String '{test}': {'Accepted' if result else 'Rejected'}")


if __name__ == "__main__":
    main()