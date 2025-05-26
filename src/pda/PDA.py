from .PDAStack import PDAStack


class PDA:
	def __init__(
		self, states, input_alphabet, stack_alphabet,
		transitions, initial_state, initial_stack_symbol,
		final_states
	):
		self.states = states
		self.input_alphabet = input_alphabet
		self.stack_alphabet = stack_alphabet
		self.transitions = transitions
		self.initial_state = initial_state
		self.initial_stack_symbol = initial_stack_symbol
		self.final_states = final_states

		self.reset()

	def reset(self):
		self.current_state = self.initial_state
		self.stack = PDAStack()
		self.stack.push(self.initial_stack_symbol)

	def step(self, input_symbol=None):
		key = (self.current_state, input_symbol, self.stack.peek())
		if key in self.transitions:
			transitions = self.transitions[key]
			if transitions:
				new_state, stack_push = transitions[0]
				self.current_state = new_state
				self.stack.pop()
				if stack_push != 'ε':
					self.stack.push(stack_push)
				return True
		return False

	def process_input(self, input_string):
		self.reset()
		idx = 0
		while idx < len(input_string):
			sym = input_string[idx]
			if self.step(sym):
				idx += 1
			elif self.step('ε'):
				continue
			else:
				return False

		while self.step('ε'):
			pass

		return self.current_state in self.final_states

	def __str__(self):
		return f"State: {self.current_state}, Stack: {self.stack}"
