from threading import Thread, Semaphore
from time import time, sleep
from Bank import *

START = time()
bank = Bank()
print_mutex = Semaphore(1)

class Customer(Thread):
	def __init__(self, customer_number, arrive_time, service_time):
		super().__init__()
		self.customer_number = customer_number
		self.arrive_time = arrive_time
		self.service_time = service_time

	def run(self):
		global START, bank
		sleep(self.arrive_time)
		ticket = bank.fetch_ticket(self.arrive_time, self.service_time)
		clerk_number = ticket.wait_for_call()
		service_begin_time = int(time() - START)
		sleep(self.service_time)
		leave_time = int(time() - START)
		print_mutex.acquire()
		print('customer_number:', self.customer_number, 'arrive_time:', 
			self.arrive_time, 'service_begin_time:', service_begin_time,
			'leave_time:', leave_time, 'clerk_number:', clerk_number)
		print_mutex.release()
		return

class Clerk(Thread):
	def __init__(self, clerk_number, work_time):
		super().__init__()
		self.clerk_number = clerk_number
		self.work_time = work_time

	def run(self):
		global START, bank
		while True:
			if time() - START > self.work_time:
				break
			ticket = bank.call_ticket()
			service_time = ticket.call(self.clerk_number)
			sleep(service_time)
		
def load_data(file_path):
	customers = []
	with open(file_path, 'r') as f:
		for i, line in enumerate(f):
			if i == 15:
				break
			customer_number, arrive_time, service_time = line.split()
			customers.append(Customer(customer_number, int(arrive_time), 
				int(service_time)))
	return customers

def generate_clerk(max_clerk, work_time = 1e2):
	clerks = []
	for i in range(max_clerk):
		clerks.append(Clerk(i + 1, work_time))
	return clerks

file_path = 'input2.txt'
customers = load_data(file_path)
clerks = generate_clerk(max_clerk = 10)

for customer in customers:
	customer.start()
for clerk in clerks:
	clerk.start()







