from threading import Thread, Lock
from datetime import datetime
from queue import Queue
import sys

from hogescraper import HogeScraper

class Counter(object):
	"""Thread-safe counter object"""
	def __init__(self):
		self._val  = 0
		self._lock = Lock()

	def increment(self):
		with self._lock:
			self._val += 1

	def decrement(self):
		with self._lock:
			self._val -= 1

	def value(self):
		return self._val

def threaded_balance_of(addrs, scraper, lock, bals, counter):
	while True:
		addr = addrs.get()
		bal  = scraper.network('eth').contract('hoge').balance_of(addr)
		#bals.put((addr, bal))
		counter.increment()
		if counter.value() % 100 == 0:
			with lock:
				sys.stdout.write("\rProcessed %d Addresses" % counter.value())
				sys.stdout.flush()
			
		addrs.task_done()

def get_address(blocks, addrs, scraper, lock, current):
	while True:
		block = blocks.get()
		try:
			end_block = (block + 1000) if (block + 1000) <= current else current
			address_filter = scraper.network('eth').contract('hoge').events().Transfer.createFilter(
				fromBlock=block,
				toBlock=end_block, 
			)
			
			txs = address_filter.get_all_entries()
		except ValueError as e:
			blocks.task_done()
			continue

		for tx in txs:
			addrs.put(tx['args']['to'])
			addrs.put(tx['args']['from'])

		with lock:
			sys.stdout.write("\rBlocks #%d-%d had %d tx's      " % (block, end_block, len(txs)))
			sys.stdout.flush()

		blocks.task_done()


def main():
	# Begin tracking execution time
	start_time   = datetime.now()
	
	# Define number of threads for each phase to instantiate
	thread_count = 20
	
	scraper      = HogeScraper('INFURA_API_KEY')
	
	# Current block number
	current      = scraper.network('eth').w3().eth.getBlock('latest')['number'] 
	# Block Hoge was deployed at
	deployed_at  = 11809212 

	# Define thread variables
	output_lock  = Lock()
	blocks       = Queue(maxsize=0)
	addrs        = Queue(maxsize=0)
	bals         = Queue(maxsize=0)
	unique_addrs = Queue(maxsize=0)
	counter      = Counter()


	# Create threadpools for each phase
	addr_pool    = [Thread(target=get_address, args=(blocks, addrs, scraper, output_lock, current)) for i in range(thread_count)]
	bal_pool     = [Thread(target=threaded_balance_of, args=(unique_addrs, scraper, output_lock, bals, counter)) for i in range(thread_count)]
	
	# Start address scraping threads
	for thread in addr_pool:
		thread.setDaemon(True)
		thread.start()		
	
	# Populate blocks Queue, 1000 block increments
	[blocks.put(i) for i in range(deployed_at, current, 1000)]

	blocks.join()
	print()
	# Filter out any duplicate address entries
	addresses   = set([addrs.get() for i in range(addrs.qsize())])
	[unique_addrs.put(addr) for addr in addresses]
	
	# Start balance scraping threads
	for thread in bal_pool:
		thread.setDaemon(True)
		thread.start()

	unique_addrs.join()

	print("\nBalances Collected: %d" % bals.qsize())
	execution = datetime.now() - start_time
	print("\nFound %d unique addresses holding Hoge" % len(addresses))
	print("Execution Time:", execution)

if __name__ == '__main__':
	main()