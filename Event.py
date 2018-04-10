class Event(object):
	def __init__(self, timestamp=None, customer=None,
	 					callback=None):
		""" Initialize data structure.
		"""
		self.timestamp = timestamp
		self.callback = callback
		self.customer = customer

	def __lt__(self, other):
		""" Comparator for ascending order according to
			timestamp of events.
		"""
		return self.timestamp < other.timestamp

	def printObj(self, customer):
		print "timestamp=%s appData=%s callback=%s customer=%s" %(
			str(self.timestamp), str(self.callback), str(self,customer))
