import numpy as np

class AbkArray:
	def __init__(self, data=[]):
		self.data = data

	def to_nd_array(self):
		return np.array(self.data)