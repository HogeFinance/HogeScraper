from statistics import mean, median, mode, stdev, variance
from threading import Thread, Lock
from datetime import datetime
from queue import Queue

from hogescraper import HogeScraper

class Counter(object):
	"""Thread-safe counter object"""

	def __init__(self) -> None:
		"""Initialize counter object"""
		self._value: int = 0
		self._lock: Lock = Lock()

	def increment(self) -> None:
		"""Increment counter by 1"""
		self.value += 1

	def decrement(self) -> None:
		"""Decrement counter by 1"""
		self.value -= 1

	@property
	def lock(self) -> Lock:
		"""Get counter lock"""
		return self._lock

	@lock.setter
	def lock(self, lock: Lock) -> None:
		"""Set counter lock"""
		self._lock: Lock = lock

	@property
	def value(self) -> int:
		"""Return current counter value"""
		return self._value

	@value.setter
	def value(self, val: int) -> None:
		"""Set counter value"""
		with self.lock:
			self._value: int = val

def threaded_balance_of(
	addrs:   Queue, 
	scraper: HogeScraper, 
	lock:    Lock, 
	bals:    Queue, 
	counter: Counter
) -> None:
	"""function to use for grabbing address balance in threads"""
	while True:
		addr: str = addrs.get()
		if addr == '': 
			addrs.task_done()
			break
		bal: str  = scraper.local.contract('hoge').balance_of(addr)
		# Uncomment below to populate bals queue
		bals.put((addr, bal))
		bals.task_done()
		counter.increment()
		if counter.value % 500 == 0:
			with lock:
				print("\rProcessed %d Addresses, Unprocessed Addresses: %d" % (counter.value, addrs.unfinished_tasks), end=" "*5)
			
		addrs.task_done()

def get_address(
	blocks:  Queue, 
	addrs:   Queue, 
	scraper: HogeScraper, 
	lock:    Lock, 
	current: int,
	filters: Counter
) -> None:
	"""function to use for grabbing address's holding hoge in threads"""
	while True:
		block: int = blocks.get()
		if block == range(0,0): 
			blocks.task_done()
			break
		try:
			end_block: int = (block + 1000) if (block + 1000) <= current else current
			address_filter: 'web3._utils.filters.LogFilter' = scraper.local.contract('hoge').events.Transfer.createFilter(
				fromBlock=block,
				toBlock=end_block, 
			)
			
			txs: list = address_filter.get_all_entries()
		except ValueError as e:
			# Filter doesnt exist ¯\_(ツ)_/¯ clear job from blocks queue and move along
			filters.increment()
			blocks.task_done()
			continue

		for tx in txs:
			addrs.put(tx['args']['to'])
			addrs.task_done()
			addrs.put(tx['args']['from'])
			addrs.task_done()

		with lock:
			print("\rBlocks #%d-%d had %d tx's, Empty filters: %d" % (block, end_block, len(txs), filters.value), end=" "*5)

		blocks.task_done()

def print_results(balances: set):
	values: list     = [i[1] for i in balances]
	gz_values: list  = [i[1] for i in values if i > 0.0]
	gt1_values: list = [i[1] for i in gz_values if i > 100.0]
	zero_addrs: list = [i for i in values if i == 0.0]

	print("Mean of Balances: %.09f" % (mean(gt1_values)))
	print("Median of Balances: %.09f" % (median(gt1_values)))
	print("Mode of Balances: %.09f" % (mode(gt1_values)))
	print("Standard Deviation of Balances: %.02f" % (stdev(gt1_values)))
	print("Variance of Balances: %.02f" % (variance(gt1_values)))
	print("0 Balance Addresses: %d" % len(zero_addrs))
	print("Balances holding more than 100 Hoge: %d" % len(gt1_values))
	print("\nFound %d unique addresses that have ever held Hoge" % len(balances))
	print("Found %d unique addresses currently holding Hoge" % len(gz_values))

def main():
	# Begin tracking execution time
	start_time: datetime.datetime = datetime.now()
	
	# Define number of threads to instantiate for each phase
	thread_count: int    = 20
	
	scraper: HogeScraper = HogeScraper('INFURA_API_KEY')
	
	# Current block number
	current: int         = scraper.local.eth.getBlock('latest')['number'] 
	# Block Hoge was deployed at
	deployed_at: int     = 11809212 

	# Define thread variables
	output_lock: Lock    = Lock()
	blocks: Queue        = Queue(maxsize=0)
	addrs: Queue         = Queue(maxsize=0)
	bals: Queue          = Queue(maxsize=0)
	counter: Counter     = Counter()
	bad_filters: Counter = Counter()

	# Create threadpools for each phase
	addr_pool: list      = [Thread(target=get_address, args=(blocks, addrs, scraper, output_lock, current, bad_filters)) for i in range(thread_count)]
	bal_pool: list       = [Thread(target=threaded_balance_of, args=(addrs, scraper, output_lock, bals, counter)) for i in range(thread_count)]
	
	# Start address scraping threads
	[thread.start() for thread in addr_pool]
		
	# Populate blocks Queue, 1000 block increments
	[blocks.put(i) for i in range(deployed_at, current, 1000)]

	# Wait for all blocks to process
	blocks.join()
	# Pass poison pill to thread and wait for threads to exit
	[blocks.put(range(0,0)) for i in range(thread_count)]
	[thread.join() for thread in addr_pool]
	blocks.join()

	print()

	# Filter out any duplicate address entries
	addresses: set = set([addrs.get() for i in range(addrs.qsize())])
	[addrs.put(addr) for addr in addresses]
	
	# Start balance scraping threads
	[thread.start() for thread in bal_pool]

	addrs.join()
	[addrs.put('') for i in range(thread_count)]
	[thread.join() for thread in bal_pool]
	addrs.join()

	print()
	
	balances: set = set([bals.get() for i in range(bals.qsize())])
	bals.join()

	print_results(balances)
	
	execution: datetime.timedelta = datetime.now() - start_time
	print("Execution Time:", execution)

if __name__ == '__main__':
	main()