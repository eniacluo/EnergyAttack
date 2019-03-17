import numpy as np
import random
import sys
import time
import socket
import json

class FSM:
	num_status = 1
	transition_matrix = np.array([])
	prior_vector = np.array([])
	cusum_prob_matrix = np.array([])
	cusum_prob_prior = np.array([])
	status_func = []

	def __init__(self, num_status, prior_vector='random', transition_matrix='random'):
		if num_status > 1:
			self.num_status = int(num_status)
			self.cusum_prob_matrix = np.zeros((self.num_status, self.num_status))
			self.cusum_prob_prior = np.zeros((self.num_status, ))
			self.status_func = [None] * int(num_status)
			if transition_matrix != 'random':
				try:
					self.transition_matrix = np.array(transition_matrix)
					transition_matrix_customized = np.array(transition_matrix)
				except Exception as e:
					self.error_print('transition_matrix parsed error.')
				if transition_matrix_customized.shape != ((self.num_status, self.num_status)):
					self.error_print('transition_matrix has wrong dimensions.')
				for i in range(self.num_status):
					prob = 0
					for j in range(self.num_status):
						prob = prob + transition_matrix_customized[i][j]
						self.cusum_prob_matrix[i][j] = prob
					if prob != 1.0:
						self.error_print('sum of line %d in transition_matrix does not equals to 1.' % i)
			else:
				transition_matrix_random = np.random.rand(self.num_status, self.num_status)
				self.transition_matrix = np.zeros((self.num_status, self.num_status))
				for i in range(self.num_status):
					norm_line = np.sum(transition_matrix_random[i])
					if norm_line != 0:
						prob = 0
						for j in range(self.num_status):
							prob = prob + (transition_matrix_random[i][j] / norm_line)
							self.cusum_prob_matrix[i][j] = prob
							self.transition_matrix[i][j] = transition_matrix_random[i][j] / norm_line
						if prob != 1.0:
							self.cusum_prob_matrix[i][self.num_status-1] = 1
					else:
						self.error_print('random numbers are all zeros.')
			if prior_vector != 'random':
				try:
					self.prior_vector = np.array(prior_vector)
					prior_vector_customized = np.array(prior_vector)
				except Exception as e:
					self.error_print('prior_vector parsed error.')
				if prior_vector_customized.shape != ((self.num_status, )):
					self.error_print('prior_vector has wrong dimension.')
				prob = 0
				for i in range(self.num_status):
					prob = prob + prior_vector_customized[i]
					self.cusum_prob_prior[i] = prob
				if prob != 1.0:
					self.error_print('sum of prior_vector does not equals to 1.')
			else:
				prior_vector_random = np.random.rand(self.num_status)
				self.prior_vector = np.zeros((self.num_status, ))
				norm_line = np.sum(prior_vector_random)
				if norm_line != 0:
					prob = 0
					for i in range(self.num_status):
						prob = prob + (prior_vector_random[i] / norm_line)
						self.cusum_prob_prior[i] = prob
						self.prior_vector[i] = prior_vector_random[i] / norm_line
					if prob != 1.0:
						self.cusum_prob_prior[self.num_status-1] = 1
				else:
					self.error_print('random numbers are all zeros.')
		else:
			self.error_print('num_status should be at least 2.')

	def bind_status_func(self, status_index, status_func):
		self.status_func[status_index] = status_func

	def run(self, max_step=100, start_status=None, max_time=0, print_status=True):
		time_start = time.time()
		step = 0
		if start_status != None:
			status = start_status
		else:
			random_cusum = random.random()
			for i in range(self.num_status):
				if random_cusum < self.cusum_prob_prior[i]:
					break
				else:
					continue
			status = i

		while (max_time == 0 or time.time() - time_start < max_time) and step <= max_step:
			if print_status == True:
				print('%8.3f [step %2d] Status = %d: %s' % (time.time()-time_start, step, status, str(self.status_func[status])))
			if self.status_func[status]:
				self.status_func[status]()
			# Choose next status
			random_cusum = random.random()
			for i in range(self.num_status):
				if random_cusum < self.cusum_prob_matrix[status][i]:
					break
				else:
					continue
			status = i
			step = step + 1

	def print_transition_matrix(self):
		print('transition_matrix:\n' + str(self.transition_matrix))
		print('prior_vector:\n' + str(self.prior_vector))

	def error_print(self, error_print):
		print('[Error] ' + error_print)
		sys.exit(1)

# Disk I/O
def write_big_files():
	for i in range(10000):
		with open('write_file.tmp', 'w+') as f:
			f.write(str([random.random()]*100))
		with open('write_file.tmp', 'r') as f_:
			f_.read()

def decompose_prime():
	i = 2
	while True:
	#if 32416187567 % i == 0:
	#    if 1299721 % i == 0:
		if 15485867 % i == 0:
	#    if 179424691 % i == 0:
			break
		else:
			i = i + 1

def write_large_array():
	for i in range(1000):
		array = []
		for j in range(10000):
			array.append(random.random())

def loopback_transferring():
	port = 13411
	socket_loopback = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	socket_loopback.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	socket_loopback.bind(('', port))
	for i in range(5000):
		try:
			socket_loopback.sendto(json.dumps([random.random()]*1000).encode('utf-8'), ('127.0.0.1', port))
			recv_data, recv_addr = socket_loopback.recvfrom(100000)
		except Exception as e:
			print('send data failed.')
			raise e

if __name__ == '__main__':
	fsm = FSM(4, prior_vector='random', transition_matrix='random')
	fsm.print_transition_matrix()
	fsm.bind_status_func(0, write_big_files)
	fsm.bind_status_func(1, decompose_prime)
	fsm.bind_status_func(2, write_large_array)
	fsm.bind_status_func(3, loopback_transferring)
	fsm.run(max_step=100)