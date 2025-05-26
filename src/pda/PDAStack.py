class PDAStack:
	def __init__(self):
		self.stack = []
	
	def push(self, symbols):
		for symbol in reversed(symbols):
			if symbol != 'ε':  # Ignore epsilon (empty string)
				self.stack.append(symbol)
	
	def pop(self):
		if len(self.stack) > 0:
			return self.stack.pop()
		return None
	
	def peek(self):
		return self.stack[-1] if self.stack else None
	
	def is_empty(self):
		return len(self.stack) == 0
	
	def __str__(self):
		return "".join(reversed(self.stack))  # Top left
