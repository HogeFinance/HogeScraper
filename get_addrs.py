from threading import Thread, Lock
from datetime import datetime
from queue import Queue
import sys

from hogescraper import HogeScraper

class Counter(object):
	"""Thread-safe counter object"""
	def __init__(self) -> None:
		"""Initialize counter object"""
		self.value = 0
		self.lock  = Lock()

	def increment(self) -> None:
		"""Increment counter by 1"""
		with self.lock:
			self.value += 1

	def decrement(self) -> None:
		"""Decrement counter by 1"""
		with self.lock:
			self.value -= 1

	@property
	def lock(self) -> Lock:
		"""Get counter lock"""
		return self._lock

	def lock(self, lock: Lock) -> None:
		"""Set counter lock"""
		self._lock = lock

	@property
	def value(self) -> int:
		"""Return current counter value"""
		return self._value

	@value.setter
	def value(self, val: int) -> None:
		"""Set counter value"""
		self._value = val

def threaded_balance_of(
	addrs: Queue, scraper: HogeScraper, 
	lock: Lock, 
	bals: Queue, 
	counter: Counter
) -> None:
	"""function to use for grabbing address balance in threads"""
	while True:
		addr: str = addrs.get()
		bal: str  = scraper.network('eth').contract('hoge').balance_of(addr)
		# Uncomment below to populate bals queue
		#bals.put((addr, bal))
		counter.increment()
		if counter.value % 100 == 0:
			with lock:
				sys.stdout.write("\rProcessed %d Addresses" % counter.value)
				sys.stdout.flush()
			
		addrs.task_done()

def get_address(
	blocks: Queue, 
	addrs: Queue, 
	scraper: HogeScraper, 
	lock: Lock, 
	current: int
) -> None:
	"""function to use for grabbing address's holding hoge in threads"""
	while True:
		block: int = blocks.get()
		try:
			end_block: int = (block + 1000) if (block + 1000) <= current else current
			address_filter: 'web3._utils.filters.LogFilter' = scraper.network('eth').contract('hoge').events.Transfer.createFilter(
				fromBlock=block,
				toBlock=end_block, 
			)
			
			txs: list = address_filter.get_all_entries()
		except ValueError as e:
			# Filter doesnt exist ¯\_(ツ)_/¯ clear job from blocks queue and move along
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
	start_time: datetime.datetime = datetime.now()
	
	# Define number of threads to instantiate for each phase
	thread_count: int    = 20
	
	scraper: HogeScraper = HogeScraper('INFURA_API_KEY')
	
	# Current block number
	current: int         = scraper.network('eth').eth.getBlock('latest')['number'] 
	# Block Hoge was deployed at
	deployed_at: int     = 11809212 

	# Define thread variables
	output_lock: Lock    = Lock()
	blocks: Queue        = Queue(maxsize=0)
	addrs: Queue         = Queue(maxsize=0)
	bals: Queue          = Queue(maxsize=0)
	unique_addrs: Queue  = Queue(maxsize=0)
	counter: Counter     = Counter()

	# Create threadpools for each phase
	addr_pool: list      = [Thread(target=get_address, args=(blocks, addrs, scraper, output_lock, current)) for i in range(thread_count)]
	bal_pool: list       = [Thread(target=threaded_balance_of, args=(unique_addrs, scraper, output_lock, bals, counter)) for i in range(thread_count)]
	
	# Start address scraping threads
	for thread in addr_pool:
		thread.setDaemon(True)
		thread.start()		
	
	# Populate blocks Queue, 1000 block increments
	[blocks.put(i) for i in range(deployed_at, current, 1000)]

	blocks.join()

	print()

	# Filter out any duplicate address entries
	addresses: set = set([addrs.get() for i in range(addrs.qsize())])
	[unique_addrs.put(addr) for addr in addresses]
	
	# Start balance scraping threads
	for thread in bal_pool:
		thread.setDaemon(True)
		thread.start()

	unique_addrs.join()

	print("\nBalances Collected: %d" % bals.qsize())
	execution: datetime.timedelta = datetime.now() - start_time
	print("\nFound %d unique addresses holding Hoge" % len(addresses))
	print("Execution Time:", execution)

if __name__ == '__main__':
	main()