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
		self.transitions_text.insert(
			tk.END,
			"(q0, a, $) -> (q0, A$)\n"
			"(q0, a, A) -> (q0, AA)\n"
			"(q0, b, A) -> (q1, ε)\n"
			"(q1, b, A) -> (q1, ε)\n"
			"(q1, ε, $) -> (q2, ε)"
		)

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
		self.fig, self.ax = plt.subplots(figsize=(4,4))
		self.canvas = FigureCanvasTkAgg(self.fig, master=diagram_frame)
		self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

		# Stack canvas for vertical stack visualization
		stack_frame = tk.LabelFrame(diagram_frame, text="Stack Visualization", padx=5, pady=5)
		stack_frame.pack(fill=tk.BOTH, expand=True)  # Changed to expand and fill
		self.stack_canvas = tk.Canvas(stack_frame, width=500, height=500, bg='white')
		self.stack_canvas.pack(fill=tk.BOTH, expand=True)  # Make it fill the frame

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
		self.stack_canvas.delete("all")  # Clear previous drawing
		
		if not self.pda:
			return
			
		stack = self.pda.stack.stack
		
		# Get actual canvas dimensions
		canvas_width = self.stack_canvas.winfo_width()
		canvas_height = self.stack_canvas.winfo_height()
		
		# If canvas isn't visible yet, use default dimensions
		if canvas_width < 10 or canvas_height < 10:
			canvas_width = 500
			canvas_height = 700
		
		# Calculate cell dimensions based on canvas size
		max_cells = 15  # Maximum number of stack elements to show
		cell_height = min(80, canvas_height // max_cells)
		cell_width = min(100, canvas_width - 100)
		x_center = canvas_width // 2
		
		# Draw stack from bottom to top
		y_position = canvas_height - 50  # Start near bottom
		
		# Draw stack base
		self.stack_canvas.create_rectangle(
			x_center - cell_width - 20, y_position + cell_height,
			x_center + cell_width + 20, y_position + cell_height + 15,
			fill="black"
		)
		
		# Draw each stack element
		for i, symbol in enumerate(stack):
			# Stop if we've reached maximum visible cells
			if i >= max_cells:
				self.stack_canvas.create_text(
					x_center, y_position - 30,
					text=f"... {len(stack)-max_cells} more items ...",
					font=("Arial", 10), fill="gray"
				)
				break
				
			# Highlight bottom and top of stack
			fill_color = "salmon" if i == 0 else "lightgreen" if i == len(stack) - 1 else "lightblue"
			outline_color = "darkred" if i == 0 else "darkgreen" if i == len(stack) - 1 else "darkblue"
			
			# Draw cell
			self.stack_canvas.create_rectangle(
				x_center - cell_width, y_position,
				x_center + cell_width, y_position + cell_height,
				fill=fill_color, outline=outline_color, width=3
			)
			
			# Draw symbol
			self.stack_canvas.create_text(
				x_center, y_position + cell_height // 2,
				text=symbol, font=("Arial", 18, "bold")
			)
			
			y_position -= cell_height + 8
		
		# Current state information
		self.stack_canvas.create_text(
			x_center, 60,
			text=f"Current State: {self.pda.current_state}",
			font=("Arial", 12), fill="black"
		)
		
		# Force canvas update
		self.stack_canvas.update_idletasks()

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
