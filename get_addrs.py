from threading import Thread, Lock
from datetime import datetime
from queue import Queue
import sys

from hogescraper import HogeScraper

class Counter(object):
	def __init__(self):
		self._val = 0
		self._lock = Lock()

	def increment(self):
		with self._lock:
			self._val += 1

	def decrement(self):
		with self._lock:
			self._val -= 1

	def value(self):
		return self._val

def threaded_balance_of(addrs, bals, scraper, lock, counter):
	while True:
		addr = addrs.get()
		bal = scraper.network('eth').contract('hoge').balance_of(addr)
		#bals.put((addr, bal))
		with lock:
			counter.increment()
			sys.stdout.write("\rProcessed %d Addresses" % counter.value())
			sys.stdout.flush()
			
		addrs.task_done()

def get_address(blocks, addrs, scraper, lock, current):
	while True:
		block = blocks.get()
		end_block = (block + 1000) if (block + 1000) <= current else current
		address_filter = scraper.network('eth').contract('hoge').contract().events.Transfer.createFilter(
			fromBlock=block,
			toBlock=end_block, 
		)
		
		txs = address_filter.get_all_entries()
		
		for tx in txs:
			addrs.put(tx['args']['to'])
			addrs.put(tx['args']['from'])

		with lock:
			sys.stdout.write("\r                              Blocks #%d-%d had %d tx's              " % (block, end_block, len(txs)))
			sys.stdout.flush()

		blocks.task_done()


def main():
	thread_count = 15
	startTime = datetime.now()
	oLock = Lock()
	blocks = Queue(maxsize=0)
	addrs = Queue(maxsize=0)
	bals = Queue(maxsize=0)
	counter = Counter()
	scraper = HogeScraper('INFURA_API_KEY')
	current = scraper.network('eth').w3().eth.getBlock('latest')['number'] # Current block number
	deployed_at = 11809212 # Block Hoge was deployed at

	thread_pool1 = [Thread(target=get_address, args=(blocks, addrs, scraper, oLock, current)) for i in range(thread_count)]
	thread_pool2 = [Thread(target=threaded_balance_of, args=(addrs, bals, scraper, oLock, counter)) for i in range(thread_count)]
	
	for thread in thread_pool1:
		thread.setDaemon(True)
		thread.start()		
	
	for thread in thread_pool2:
		thread.setDaemon(True)
		thread.start()
	
	# Populate blocks Queue, 1000 block increments
	[blocks.put(i) for i in range(deployed_at, current, 1000)]

	blocks.join()
	
	#addresses = set([addrs.get() for i in range(addrs.qsize())])
	#[addrs.put(addr) for addr in addresses]
	
	print()

	addrs.join()
	execution = datetime.now() - startTime
	#print(addresses)
	print("\nFound %d unique addresses holding Hoge" % counter.value())
	print("Execution Time:", execution)

if __name__ == '__main__':
	main()