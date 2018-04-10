from collections import deque
class Pay(object):
	def __init__(self, num_of_checkout_lines=4, capacity_per_line=16):

		# queue for checkout
		self.lines = [deque() for _ in xrange(num_of_checkout_lines)]
		self.checkout_time = {"credit_card": 50, "buzzcard": 40, "cash": 80}
		self.num_of_checkout_lines = num_of_checkout_lines
		self.capacity_per_line = capacity_per_line

	def isFull(self):
		for line in self.lines:
			if len(line) < self.capacity_per_line:
				return False
		return True

	def add_one(self, customer):
		""" Add one customer to shortest queue
		"""
		if self.isFull():
			return -1
		val, idx = min((len(line), idx) for (idx, line) in enumerate(self.lines))
		assert 0 < len(self.lines[idx]) < self.capacity_per_line
		self.lines[idx].append(customer)
		customer.checkout_line = idx	# add ckechout_line number to customer
		return 1

	def emptyLine(self):
		"""
		If any line is empty, return its line number.
		Else, return -1.
		"""
		for i, line in enumerate(self.lines):
			if len(line) == 0:
				return i
		return -1
