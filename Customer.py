from random import random, seed

class Customer(object):
	def __init__(self, id, arrival_time):
		self.id = id
		self.payment_method = ""
		self.drinks = False

		self.set_payment_method()
		self.set_drink()
		self.set_restaurant()
		self.checkout_line = -1
		self.time = {
			"arrival": arrival_time,
			"serve": -1,
			"serve_drinks": -1,
			"finish_drinks": -1,
			"finish_serving": -1,
			"checkout": -1,
			"finish_checkout": -1
		}
		

	def set_payment_method(self):
		# "credit_card", "buzzcard", or "cash"
		#      30%           60%         10%
		rand = random()
		if rand < 0.3:
			self.payment_method = "credit_card"
		elif rand < 0.9:
			self.payment_method = "buzzcard"
		else:
			self.payment_method = "cash"

	def set_drink(self):
		rand = random()
		if rand < 0.2:
			self.drinks = True
		else:
			self.drinks = False

	def set_restaurant(self):
		idx = int(random() * 7)
		all_restaurants = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		self.restaurant = all_restaurants[idx]
