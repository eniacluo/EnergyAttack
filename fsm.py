import numpy as np

class FSM:
	transition_matrix = np.array([])
	status_func = []

	def __init__(self, num_status, transition_matrix='random'):


	def bind_status_func(self, status_index, status_func):
		pass

	def run(self, max_step=100, print_status=True):
		pass