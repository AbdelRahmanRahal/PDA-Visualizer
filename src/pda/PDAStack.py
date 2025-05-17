class PDAStack:
	def __init__(self):
		"""Initialize the PDA stack with a bottom marker (typically '$')."""
		self.stack = ['$']
	
	def push(self, symbols):
		"""Push symbols onto the stack (in reverse order for correct processing)."""
		# Push symbols in reverse order to maintain correct stack order
		for symbol in reversed(symbols):
			if symbol != 'ε':  # Don't push empty string
				self.stack.append(symbol)
	
	def pop(self):
		"""Pop the top symbol from the stack."""
		if len(self.stack) > 1:  # Don't pop the bottom marker
			return self.stack.pop()
		return None  # Or raise an exception for empty stack
	
	def peek(self):
		"""Return the top symbol without popping it."""
		return self.stack[-1] if len(self.stack) > 0 else None
	
	def is_empty(self):
		"""Check if stack only contains the bottom marker."""
		return len(self.stack) == 1
	
	def __str__(self):
		return "".join(reversed(self.stack))  # Display with top symbol first