from Restaurant import Restaurant
from collections import deque
from Pay import Pay

class Application(object):

	def __init__(self, FEL):

		self.restaurants = {
			'a': Restaurant(),
			'b': Restaurant(),
			'c': Restaurant(),
			'd': Restaurant(),
			'e': Restaurant(),
			'f': Restaurant(),
			'g': Restaurant(),
			'drinks': Restaurant(availability=2)
		}
		self.be4 = deque()
		self.pay = Pay(num_of_checkout_lines = 8)
		self.FEL = FEL
		self.poisson_mean = 4
		self.be4_capacity = 50
		self.customers = []

		self.debug = 1

	def arrival(self, event):
		""" Customers arrive at the food court.
		"""
		customer = event.customer

		# if either Food Court (be4 queue) or all restaurants are full,
		def restaurant_full():
			return all(self.restaurants[rest].full() for rest in ['a', 'b', 'c', 'd', 'e', 'f', 'g'])

		# customer goes away
		if len(self.be4) > self.be4_capacity or restaurant_full():
			# print "be4 size: %d" % (len(self.be4))
			# for i in range(4):
			# 	print "checkout line %d: %d" % (i, len(self.pay.lines[i]))
			# print "Restaurant Full: ", restaurant_full()
			if self.debug:
				print "--------------------------------"
				print "Customer %d went away at time %d" % (customer.id, event.timestamp)
				print "Restaurant Full: ", restaurant_full()
				print "Queue before checkout Full: ", len(self.be4) > self.be4_capacity
				# print "Queue before checkout Full: ", len(self.be4) > self.be4_capacity, "(%d/%d)" % (len(self.be4), self.be4_capacity)
				print "--------------------------------"
			return
		# for i in range(4):
		# 	print "checkout line %d: %d" % (i, len(self.pay.lines[i]))
		# customer changes restaurant

		while len(self.restaurants[customer.restaurant].queue) >= self.restaurants[customer.restaurant].capacity:
			customer.set_restaurant()

		# if available, don't go into queue
		if self.restaurants[customer.restaurant].availability > 0:
			self.restaurants[customer.restaurant].availability -= 1
			# schedule the next serve_food event
			self.FEL.schedule(event.timestamp, customer, self.serve)
		# if not available wait in queue
		else:
			self.restaurants[customer.restaurant].queue.append(customer)

	def serve(self, event):
		""" Restaurant serving the customers.
		"""
		customer = event.customer
		restaurant = customer.restaurant
		# Must be serving food
		if customer.time['serve'] == -1:
			customer.time['serve'] = event.timestamp
		else:
			restaurant = "drinks"
			customer.time['serve_drinks'] = event.timestamp
		# if there is someone waiting in the queue_food

		after_serving_time = event.timestamp + self.restaurants[restaurant].serving_fast
		# Schedule for finish_serving
		if restaurant != "drinks":
			self.FEL.schedule(after_serving_time, customer, self.finish_serving)
		else:
			self.FEL.schedule(after_serving_time, customer, self.finish_drinks)

	def turn(self, event):
		""" Customers move from be4 queue to paying queue.
		"""
		empty_line_num = self.pay.emptyLine()
		event.customer.time["turn"] = event.timestamp

		if empty_line_num != -1 : # there is an empty line
			# add customer to that queue
			assert len(self.pay.lines[empty_line_num]) == 0
			self.pay.lines[empty_line_num].append(event.customer)
			event.customer.checkout_line = empty_line_num	# record line# in customer

			# schedule checkout evnet for itself
			self.FEL.schedule(event.timestamp, event.customer, self.checkout)

		else:	# no empty line
			if self.pay.add_one(event.customer) == -1:
				self.be4.append(event.customer)


	def finish_drinks(self, event):
		""" Customer finishes filling up their drinks.
		"""

		# put himself to be4 queue
		event.customer.time["finish_drinks"] = event.timestamp
		if not self.be4:
			self.FEL.schedule(event.timestamp, event.customer, self.turn)
		else:
			self.be4.append(event.customer)

		"""
		If no one at the drinking queue, free up machine availablilty.
		If people in queue, schedule next one's finish_drinks event.
		"""
		if len(self.restaurants['drinks'].queue) == 0:
			# 1 machine will be free for next customer
			self.restaurants['drinks'].availability += 1
		else:
			# schedule next finish_drinks
			customer = self.restaurants['drinks'].queue.popleft()
			# self.FEL.schedule(event.timestamp + self.restaurants['drinks'].serving_fast,
			# 	customer, self.finish_drinks)

			# In the drinks queue means it has been served with food
			# serve again will guarantee to serve drinks
			self.FEL.schedule(event.timestamp, customer, self.serve)

	def checkout(self, event):
		""" Customers start checkout.
		"""
		customer = event.customer
		customer.time['checkout'] = event.timestamp
		after_checkout_time = event.timestamp + self.pay.checkout_time[customer.payment_method]

		c1 = self.pay.lines[customer.checkout_line][0]
		if self.debug:
			print "customer %d checkout at line %d at time %d" % (customer.id, customer.checkout_line, event.timestamp)
			# print "customer id: %d == %d" % (c1.id, customer.id)
			# print ""

		assert customer.id == c1.id

		self.FEL.schedule(after_checkout_time, customer, self.finish_checkout)

	def finish_checkout(self, event):
		""" Customers finish checkout.
		"""
		# event.customer.time["finish_checkout"] = event.timestamp

		customer = event.customer
		checkout_line = customer.checkout_line
		customer.time['finish_checkout'] = event.timestamp
		# print len(self.pay.lines[checkout_line])
		## Do some statistics things
		#pass

		# Checkout for the customer
		# print len(self.pay.lines[checkout_line])
		c1 = self.pay.lines[checkout_line].popleft()
		if self.debug:
			print "customer %d finish_checkout at line %d at time %d" % (customer.id, checkout_line, event.timestamp)
			# print "id: %d == %d" % (c1.id, customer.id)
			# print ""
		assert c1.id == customer.id

		# next_timestamp = event.timestamp + self.pay.checkout_time[customer.payment_method]
		self.customers.append(customer)

		# Pull somebody from the be4 if there's any,
		if self.be4:
			new_customer = self.be4.popleft()
			new_customer.checkout_line = checkout_line
			self.pay.lines[checkout_line].append(new_customer)
		if self.pay.lines[checkout_line]:
			self.FEL.schedule(event.timestamp, self.pay.lines[checkout_line][0], self.checkout)


	def finish_serving(self, event):
		""" finish servering at food station, and send to queue_pay to wait for checkout
		"""

		timestamp = event.timestamp
		customer = event.customer
		customer.time['finish_serving'] = event.timestamp
		restaurant = customer.restaurant

		# schedule for next serve if there exists one
		# if not, set serve availability ++
		if self.restaurants[restaurant].queue:
			next_customer = self.restaurants[restaurant].queue.popleft()
			self.FEL.schedule(timestamp, next_customer, self.serve)
		else:
			self.restaurants[restaurant].availability += 1

		# if the served customer needs drinks, send him to drink
		# else, send him to be4
		if customer.drinks:
			if self.restaurants['drinks'].availability > 0:
				self.restaurants['drinks'].availability -= 1
				# In the drinks queue means it has been served with food
				# serve again will guarantee to serve drinks
				self.FEL.schedule(timestamp, customer, self.serve)
			else:
				self.restaurants['drinks'].queue.append(customer)
		else:
			# if be4 empty, schedule TURN
			if not self.be4:
				self.FEL.schedule(timestamp, customer, self.turn)
			else:
				self.be4.append(customer)



		# # add customer to queue
		# heapq.heappush(self.panda_attribute.queue_pay, customer)

		# check if there is no one in the queue
		# if self.panda_attribute.queue_pay:
		# 	# people in from of you will schedule event for you.
		# 	pass
		# else:
		# 	schedule(timestamp, customer, self.checkout)
