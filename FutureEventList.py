
import heapq
from Event import Event

class FutureEventList(object):
	"""
	Engine for discrete event simulation.
	"""

	def __init__(self):
		self.FEL = []

	def isEmpty(self):
		return len(self.FEL) == 0

	def schedule(self, timestamp, customer, callback):
		""" pq specifies which queue to schedule in.
		"""
		e = Event(timestamp, customer, callback)
		heapq.heappush(self.FEL, e)

	def pop(self):
		""" Exactly like remove, just to match python style
		"""
		return self.remove()

	def remove(self):
		""" Remove the smallest event in queue_food, queue_pay, and
			queue_drink.
			ps. Like pop, matches professor's function style
		"""
		if self.FEL:
			return heapq.heappop(self.FEL)
		return None

