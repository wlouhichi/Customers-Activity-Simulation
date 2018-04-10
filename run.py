from time import time
from FutureEventList import FutureEventList
from Application import Application
from util import generate_statistics
from Customer import Customer
import numpy as np

def run_simulation(FEL):
	while not FEL.isEmpty():
		event = FEL.pop()
		# NOW = event.timestamp
		event.callback(event)
		# PrintList(FEL_HEAD)
		# print "now:", gb.Now

def main():
	# engine = Engine(app)
	FEL = FutureEventList()
	app = Application(FEL)
        
	print "Schedule for ALL the arrivals"
	poissons = np.random.poisson(app.poisson_mean, 10000)
	timestamp = 0
	i = 0
	# timestamps = np.cumsum(np.random.poisson(poisson_mean, size))
	customers = []
	while timestamp < 7200:
		customers.append(Customer(i, timestamp))
		timestamp += poissons[i]
		i += 1

	for j in range(i):
		FEL.schedule(customers[j].time['arrival'], customers[j], app.arrival)
	# FEL.schedule(Event(timestamp, Customer(), app.arrival_food))


	# print "Schedule for First Order at", timestamp
	# engine.schedule(timestamp,
	# 				data = "testAppData",
	# 				callback = app.arrival_food,
	# 				pq = app.panda_attribute.queue_food)



	start_time = time()
	# engine.run_simulation()
	run_simulation(FEL)
	total_run_time = (time() - start_time)

	generate_statistics(customers)
	# print "==================="
	# print "Total Running Time: %d" % (total_run_time)
	# for i, customer in enumerate(customers):
	# 	print "Customer %d" % customer.id
	# 	print customer.restaurant
	# 	print customer.drinks
	# 	print customer.payment_method
	# 	print customer.time['arrival']
	# 	print customer.time['serve']
	# 	print customer.time['finish_serving']
	# 	if customer.drinks:
	# 		print customer.time['serve_drinks']
	# 		print customer.time['finish_drinks']
	#
	# 	print customer.time['finish_checkout']

	# print ""
	# print "=== statistics ==="
	# print "Number of orders = %d" % OrderCount
	# print "Total waiting time = %f" % TotalWaitingTime
	# print "Average waiting time = %f" % (TotalWaitingTime/ float(N_Orders))
	# print "%d events executed in %f seconds (%f events per second)" % (NEvents, total_run_time, float(NEvents) / total_run_time)
	# print ""

if __name__ == "__main__":
	main()
