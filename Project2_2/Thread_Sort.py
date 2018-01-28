from queue import Queue
from threading import Thread, Lock, Semaphore
import threading
from time import time, sleep

Numbers = []
thread_num = 20
lock = Lock()
with open('Randoms.txt', 'r') as f:
	for line in f:
		Numbers.append(float(line))

class Thread_Job(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end	
	
	def do_job(self, work_queue, work_num):
		global Numbers, lock
		with lock:
			numbers = Numbers[self.start:self.end]
		if len(numbers) < 1000:
			with lock:
				Numbers[self.start:self.end] = sorted(numbers)
		else:
			base = numbers[-1]
			less, equal, greater = [], [], []
			for i in numbers:
				if i < base:
					less.append(i)
				elif i == base:
					equal.append(i)
				else:
					greater.append(i)
			numbers = less + equal + greater
			with lock:
				Numbers[self.start:self.end] = numbers
			work_queue.put(Thread_Job(self.start, self.start + len(less)))
			work_queue.put(Thread_Job(self.end - len(greater), self.end))
			work_num.release()
			work_num.release()
		return work_queue, work_num

class Thread_Pool_Manager(object):
	def __init__(self, thread_num):
		self.thread_num = thread_num
		self.work_queue = Queue()
		self.work_num = Semaphore(0)
		self.mutex = Lock()

	def start_threads(self):
		for i in range(self.thread_num):
			thread = Thread(target = self.do_job)
			thread.daemon = True	# set thread as daemon
			thread.start()

	def do_job(self):
		while True:
			self.work_num.acquire()
			with self.mutex:
				thread_job = self.work_queue.get()
			self.work_queue, self.work_num = thread_job.do_job(self.work_queue,
				self.work_num)		
			self.work_queue.task_done()

	def join(self):
		self.work_queue.join()

	def add_job(self, job):
		self.work_queue.put(job)
		self.work_num.release()

thread_pool_manager = Thread_Pool_Manager(thread_num)
thread_pool_manager.add_job(Thread_Job(0, len(Numbers)))
thread_pool_manager.start_threads()
start_time = time()
thread_pool_manager.join()
print('sort time:', time() - start_time)

with open('Sorted_Numbers.txt', 'w') as f:
	for number in Numbers:
		print('{:6f}'.format(number), file = f)
print('file saved!')









