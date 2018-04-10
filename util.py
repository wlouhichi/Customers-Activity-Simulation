import unittest
import math, random
import numpy as np

def generate_statistics(customers):
	# total customers
	# number of people go away
	# average waiting time
	# standard deviation of waiting time
	# wait for serving / wait for checkout
	print "Total Customers: %d" % len(customers)

	customers_stayed = [customer for customer in customers if customer.time['serve'] != -1]
	print "Total Customers go away: %d" % (len(customers) - len(customers_stayed))

	def separate_time(customer):
		return customer.time['finish_drinks'] if customer.drinks else customer.time['finish_serving']
	wait_serving_times = np.array([ separate_time(customer)
						- customer.time['arrival'] for customer in customers_stayed])
	wait_checkout_times = np.array([customer.time['finish_checkout']\
						- separate_time(customer) for customer in customers_stayed])

	all_wait_times = wait_serving_times + wait_checkout_times

	print "Wait for Serving Time:"
	print "Average: %f" % wait_serving_times.mean()
	print "Standard Deviation: %f" % wait_serving_times.std()
	print "------------------------------"

	print "Wait for Checkout Time:"
	print "Average: %f" % wait_checkout_times.mean()
	print "Standard Deviation: %f" % wait_checkout_times.std()
	print "------------------------------"

	print "All Waiting Time:"
	print "Average: %f" % all_wait_times.mean()
	print "Standard Deviation: %f" % all_wait_times.std()
	print "------------------------------"

def print_queue_timestamp(q):
	print [e.timestamp for e in q]