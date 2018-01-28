from queue import Queue
# from threading import Thread, Lock, Semaphore
import threading
from time import time, sleep
from multiprocessing import Process, Lock, Semaphore, cpu_count, JoinableQueue

Numbers = []
lock = Lock()
with open('Randoms.txt', 'r') as f:
	for j, line in enumerate(f):
		if j == 50:
			break
		Numbers.append(float(line))

class Thread_Job(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end	
	
	def do_job(self, work_queue, work_num):
		global Numbers, lock
		with lock:
			numbers = Numbers[self.start:self.end]
		if len(numbers) < 5:
			with lock:
				Numbers[self.start:self.end] = sorted(numbers)
				# print(sorted(numbers))
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

class Thread_Pool_Manager(object):
	def __init__(self, thread_num = cpu_count()):
		self.thread_num = thread_num
		print(thread_num)
		self.work_queue = JoinableQueue()
		self.work_num = Semaphore(0)
		self.mutex = Lock()

	def start_threads(self):
		for i in range(self.thread_num):
			thread = Process(target = self.do_job)
			thread.daemon = True	# set thread as daemon
			thread.start()

	def do_job(self):
		global Numbers
		while True:
			# print(1)
			self.work_num.acquire()
			with self.mutex:
				print(1, self.work_queue.qsize())
				thread_job = self.work_queue.get()
				print(0, self.work_queue.qsize())
			thread_job.do_job(self.work_queue, self.work_num)
			print(self.work_queue.qsize())
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

with open('Sorted_Numbers_tmp.txt', 'w') as f:
	for number in Numbers:
		print('{:6f}'.format(number), file = f)
print('file saved!')









