class PDA:

    def __init__(self, states, input_symbols, stack_symbols, transitions, start_state, start_stack, accept_states):
        
        # Initialize the PDA with states, input symbols, stack symbols, transitions, start state, start stack, and accept states
        # states: Set of states
        # input_symbols: Set of input symbols
        # stack_symbols: Set of stack symbols
        # transitions: Dictionary mapping (state, input_symbol, stack_top) to list of (next_state, stack_push)
        # start_state: Initial state
        # start_stack: Initial stack symbol $ or z0
        # accept_states: Set of accept states
        
      
        self.states = states
        self.input_symbols = input_symbols
        self.stack_symbols = stack_symbols
        self.transitions = transitions  
        self.start_state = start_state
        self.start_stack = start_stack
        self.accept_states = accept_states

    def accepts(self, input_string):
        # Check if the input string is accepted by the PDA
        stack = [self.start_stack]
        return self._accept_recursive(self.start_state, input_string, stack)

    def _accept_recursive(self, state, remaining_input, stack):
        # Recursive function to check if the PDA can accept the input string
        
        if not remaining_input and state in self.accept_states:
            return True

        key = (state, remaining_input[:1] if remaining_input else '', stack[-1] if stack else '')
        options = self.transitions.get(key, [])

        for next_state, stack_action in options:
            new_stack = stack[:-1] if stack else []
            new_stack.extend(reversed(stack_action))
            if self._accept_recursive(next_state, remaining_input[1:], new_stack):
                return True

        return False


def parse_pda_config(config):
    # Placeholder: Parse PDA configuration from a dictionary or file
    return PDA(
        states=config['states'],
        input_symbols=config['input_symbols'],
        stack_symbols=config['stack_symbols'],
        transitions=config['transitions'],
        start_state=config['start_state'],
        start_stack=config['start_stack'],
        accept_states=config['accept_states']
    )
