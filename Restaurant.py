from collections import deque

class Restaurant(object):
	''' Define parameter in the class
	'''
	def __init__(self, serving_fast=60, serving_slow=90, availability=1, restaurant_capacity=20, close_time=7200):
		''' Default parameters are defined below
		'''
		# self.now = 0
		self.close_time = close_time # 2 hours * 3600 sec

		self.queue = deque()

		self.capacity = restaurant_capacity
		self.availability = availability

		self.serving_fast = serving_fast
		self.serving_slow = serving_slow

	def full(self):
		return len(self.queue) >= self.capacity

	def welcome(self):
		print ""
		print "=== Welcome to Student Center Food Court Simulation ==="
