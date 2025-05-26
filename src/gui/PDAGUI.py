import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pda.PDA import PDA


class PDAGUI:
	def __init__(self, root):
		self.root = root
		self.root.title("PDA Simulator with Stack Visualization")
		self.root.geometry("1100x700")

		control_frame = tk.Frame(root, padx=10, pady=10)
		control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		diagram_frame = tk.Frame(root, padx=10, pady=10)
		diagram_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		# PDA config inputs
		config_frame = tk.LabelFrame(control_frame, text="PDA Configuration", padx=5, pady=5)
		config_frame.pack(fill=tk.BOTH, expand=True)

		labels = ["States (comma-separated):",
				  "Input Alphabet (comma-separated):",
				  "Stack Alphabet (comma-separated):",
				  "Initial State:",
				  "Initial Stack Symbol:",
				  "Final States (comma-separated):"]

		self.entries = {}
		for i, label in enumerate(labels):
			tk.Label(config_frame, text=label).grid(row=i, column=0, sticky='w', pady=2)
			entry = tk.Entry(config_frame, width=30)
			entry.grid(row=i, column=1, pady=2)
			self.entries[label] = entry

		tk.Label(config_frame, text="Transitions (one per line):").grid(row=len(labels), column=0, sticky='w', pady=2)
		self.transitions_text = tk.Text(config_frame, width=40, height=8)
		self.transitions_text.grid(row=len(labels), column=1, pady=2)
		self.transitions_text.insert(tk.END, "(q0, a, $) -> (q0, A$)\n(q0, a, A) -> (q0, AA)\n(q0, b, A) -> (q1, ε)\n(q1, b, A) -> (q1, ε)\n(q1, ε, $) -> (q2, $)")

		# Simulation controls
		sim_frame = tk.LabelFrame(control_frame, text="Simulation", padx=5, pady=5)
		sim_frame.pack(fill=tk.BOTH, expand=True, pady=10)

		tk.Label(sim_frame, text="Input String:").grid(row=0, column=0, sticky='w')
		self.input_entry = tk.Entry(sim_frame, width=30)
		self.input_entry.grid(row=0, column=1, pady=5)

		self.step_button = tk.Button(sim_frame, text="Step", command=self.step)
		self.step_button.grid(row=1, column=0, pady=5)

		self.run_button = tk.Button(sim_frame, text="Run", command=self.run)
		self.run_button.grid(row=1, column=1, pady=5)

		self.reset_button = tk.Button(sim_frame, text="Reset", command=self.reset)
		self.reset_button.grid(row=1, column=2, pady=5)

		self.status_label = tk.Label(sim_frame, text="Status: Ready")
		self.status_label.grid(row=2, column=0, columnspan=3, sticky='w')

		self.current_input_pos = 0

		# PDA diagram canvas
		self.fig, self.ax = plt.subplots(figsize=(5,5))
		self.canvas = FigureCanvasTkAgg(self.fig, master=diagram_frame)
		self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

		# Stack canvas for vertical stack visualization
		stack_frame = tk.LabelFrame(diagram_frame, text="Stack Visualization", padx=5, pady=5)
		stack_frame.pack(fill=tk.BOTH, expand=False)
		self.stack_canvas = tk.Canvas(stack_frame, width=150, height=350, bg='white')
		self.stack_canvas.pack()

		self.pda = None
		self.transitions = {}

		self.draw_nx_graph_placeholder()

	def draw_nx_graph_placeholder(self):
		self.ax.clear()
		self.ax.text(0.5, 0.5, "PDA Diagram will appear here", ha='center', va='center', fontsize=12)
		self.ax.axis('off')
		self.canvas.draw()

	def parse_transitions(self, text):
		transitions = {}
		lines = text.strip().split('\n')
		for line in lines:
			if '->' not in line:
				continue
			left, right = line.split('->')
			left = left.strip()[1:-1]  # remove parentheses
			right = right.strip()[1:-1]
			state, inp, stack_top = [x.strip() for x in left.split(',')]
			new_state, stack_push = [x.strip() for x in right.split(',')]
			key = (state, inp, stack_top)
			if key not in transitions:
				transitions[key] = []
			transitions[key].append((new_state, stack_push))
		return transitions

	def load_pda(self):
		try:
			states = [s.strip() for s in self.entries["States (comma-separated):"].get().split(',')]
			input_alpha = [s.strip() for s in self.entries["Input Alphabet (comma-separated):"].get().split(',')]
			stack_alpha = [s.strip() for s in self.entries["Stack Alphabet (comma-separated):"].get().split(',')]
			initial_state = self.entries["Initial State:"].get().strip()
			initial_stack_symbol = self.entries["Initial Stack Symbol:"].get().strip()
			final_states = [s.strip() for s in self.entries["Final States (comma-separated):"].get().split(',')]
			self.transitions = self.parse_transitions(self.transitions_text.get("1.0", tk.END))
			self.pda = PDA(states, input_alpha, stack_alpha, self.transitions, initial_state, initial_stack_symbol, final_states)
			self.draw_pda_graph()
			self.current_input_pos = 0
			self.status_label.config(text="Status: PDA Loaded. Ready.")
			self.update_stack_visual()
		except Exception as e:
			messagebox.showerror("Error", f"Failed to load PDA:\n{e}")

	def draw_pda_graph(self):
		self.ax.clear()
		G = nx.DiGraph()
		for s in self.pda.states:
			G.add_node(s)
		for (state, inp, stack_top), dests in self.transitions.items():
			for (new_state, stack_push) in dests:
				label = f"{inp}, {stack_top} -> {stack_push}"
				G.add_edge(state, new_state, label=label)
		pos = nx.spring_layout(G)
		nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=1500, node_color='lightblue')
		edge_labels = nx.get_edge_attributes(G, 'label')
		nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)
		self.canvas.draw()

	def update_stack_visual(self):
		self.stack_canvas.delete("all")
		if not self.pda:
			return
		stack = self.pda.stack.stack

		box_width = 100
		box_height = 30
		x = 25
		y_start = 320  # bottom margin

		# Draw stack boxes from bottom (stack[0]) to top (stack[-1])
		for i, symbol in enumerate(stack):
			y = y_start - (len(stack) - 1 - i) * box_height
			self.stack_canvas.create_rectangle(x, y - box_height, x + box_width, y, fill='lightyellow', outline='black')
			self.stack_canvas.create_text(x + box_width/2, y - box_height/2, text=symbol, font=('Arial', 16))

		# Label top of stack
		self.stack_canvas.create_text(x + box_width + 20, y_start - (len(stack) - 1) * box_height + 15,
									 text="Top", fill="red", font=('Arial', 12, 'bold'))

	def step(self):
		if not self.pda:
			self.load_pda()
			if not self.pda:
				return

		input_string = self.input_entry.get()
		if self.current_input_pos >= len(input_string):
			# Try epsilon transitions after input consumed
			if not self.pda.step('ε'):
				accepted = self.pda.current_state in self.pda.final_states and self.pda.stack.is_empty()
				self.status_label.config(text=f"Input consumed. Final state: {self.pda.current_state}. Accepted: {accepted}")
				messagebox.showinfo("Result", "Accepted" if accepted else "Rejected")
				return
		else:
			symbol = input_string[self.current_input_pos]
			success = self.pda.step(symbol)
			if not success:
				self.status_label.config(text=f"Rejected at input position {self.current_input_pos} (symbol '{symbol}')")
				messagebox.showinfo("Result", "Rejected")
				return
			self.current_input_pos += 1

		self.status_label.config(text=f"Current State: {self.pda.current_state}, Next Input Pos: {self.current_input_pos}")
		self.update_stack_visual()

	def run(self):
		if not self.pda:
			self.load_pda()
			if not self.pda:
				return
		input_string = self.input_entry.get()
		self.pda.reset()
		self.current_input_pos = 0
		accepted = True
		for symbol in input_string:
			if not self.pda.step(symbol):
				accepted = False
				break
			self.current_input_pos += 1
			self.update_stack_visual()
			self.status_label.config(text=f"Current State: {self.pda.current_state}, Input pos: {self.current_input_pos}")
			self.root.update()  # Refresh UI
			self.root.after(300)  # Pause for visibility

		# After input processed, apply epsilon transitions
		while accepted and self.pda.step('ε'):
			self.update_stack_visual()
			self.status_label.config(text=f"Current State: {self.pda.current_state}, Epsilon transitions")
			self.root.update()
			self.root.after(300)

		accepted = accepted and (self.pda.current_state in self.pda.final_states and self.pda.stack.is_empty())
		self.status_label.config(text=f"Run finished. Accepted: {accepted}")
		messagebox.showinfo("Result", "Accepted" if accepted else "Rejected")

	def reset(self):
		self.pda = None
		self.current_input_pos = 0
		self.status_label.config(text="Status: Ready")
		self.input_entry.delete(0, tk.END)
		self.stack_canvas.delete("all")
		self.draw_nx_graph_placeholder()
