from threading import Semaphore
from operator import attrgetter

class Bank(object):
	def __init__(self):
		self.mutex = Semaphore(1)
		self.ticket_num = Semaphore(0)
		self.tickets = []

	def fetch_ticket(self, arrive_time, service_time):
		self.mutex.acquire()
		ticket = Ticket(arrive_time, service_time)
		self.tickets.append(ticket)
		self.ticket_num.release()
		self.mutex.release()
		return ticket

	def call_ticket(self):
		self.ticket_num.acquire()
		self.mutex.acquire()
		self.tickets.sort(key = attrgetter('arrive_time', 
			'service_time'), reverse = True)
		# self.tickets.sort(key = attrgetter('service_time'),
			# reverse = True)
		ticket = self.tickets.pop()
		self.mutex.release()
		return ticket

class Ticket(object):
	def __init__(self, arrive_time, service_time):
		self.clerk = Semaphore(0)
		self.arrive_time = arrive_time
		self.service_time = service_time
		self.clerk_number = None

	def wait_for_call(self):
		self.clerk.acquire()		# judge whether a clerk call this ticket
		return self.clerk_number

	def call(self, clerk_number):
		self.clerk_number = clerk_number
		self.clerk.release()
		return self.service_time

