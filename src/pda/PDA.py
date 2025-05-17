from PDAStack import PDAStack

class PDA:
    def __init__(self, states, input_alphabet, stack_alphabet, 
                 transitions, initial_state, initial_stack_symbol, 
                 final_states):
        """
        Initialize the PDA.
        
        Parameters:
        - states: set of states
        - input_alphabet: set of input symbols
        - stack_alphabet: set of stack symbols
        - transitions: dictionary of transitions in the form:
            {(state, input_symbol, stack_top): [(new_state, stack_push), ...], ...}
        - initial_state: starting state
        - initial_stack_symbol: initial stack symbol (should be in stack_alphabet)
        - final_states: set of accepting states
        """
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.initial_stack_symbol = initial_stack_symbol
        self.final_states = final_states
        self.current_state = initial_state
        self.stack = PDAStack()
        self.stack.push(initial_stack_symbol)  # Initialize stack
        
    def reset(self):
        """Reset the PDA to its initial configuration."""
        self.current_state = self.initial_state
        self.stack = PDAStack()
        self.stack.push(self.initial_stack_symbol)
    
    def step(self, input_symbol):
        """
        Process one input symbol.
        
        Returns:
        - True if transition was successful
        - False if no valid transition
        """
        stack_top = self.stack.peek()
        key = (self.current_state, input_symbol, stack_top)
        
        # Check for explicit transitions
        if key in self.transitions:
            # For non-deterministic PDA, we'd explore all possibilities
            # Here we just take the first transition for simplicity
            new_state, stack_push = self.transitions[key][0]
            self.current_state = new_state
            self.stack.pop()
            self.stack.push(stack_push)
            return True
        
        # Check for epsilon transitions (empty input)
        epsilon_key = (self.current_state, 'ε', stack_top)
        if epsilon_key in self.transitions:
            new_state, stack_push = self.transitions[epsilon_key][0]
            self.current_state = new_state
            self.stack.pop()
            self.stack.push(stack_push)
            return True
        
        return False
    
    def process_input(self, input_string):
        """
        Process an entire input string.
        
        Returns:
        - True if the input is accepted
        - False otherwise
        """
        self.reset()
        
        for symbol in input_string:
            if not self.step(symbol):
                return False
        
        # Check if current state is final (accept by final state)
        if self.current_state in self.final_states:
            return True
        
        # Alternatively, could check for empty stack (accept by empty stack)
        # return self.stack.is_empty()
        
        return False
    
    def visualize(self, input_string=None):
        """Visualize the PDA's current configuration."""
        print(f"Current State: {self.current_state}")
        print(f"Stack: {self.stack}")
        if input_string:
            print(f"Remaining Input: {input_string}")
        print("---")
