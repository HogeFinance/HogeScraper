from threading import Thread, Lock
from queue import Queue
import sys

from hogescraper import HogeScraper

def get_address(blocks, addrs, scraper, lock):
	while True:
		block = blocks.get()
		address_filter = scraper.network('eth').contract('hoge').contract().events.Transfer.createFilter(
			fromBlock=block,
			toBlock=block+1000, 
		)
		
		txs = address_filter.get_all_entries()
		
		for tx in txs:
			addrs.put(tx['args']['to'])
			addrs.put(tx['args']['from'])

		with lock:
			sys.stdout.write('\rBlock #%d had %d tx\'s' % (block, len(txs)))
			sys.stdout.flush()

		blocks.task_done()


def main():
	oLock = Lock()
	blocks = Queue(maxsize=0)
	addrs = Queue(maxsize=0)
	scraper = HogeScraper('INFURA_API_KEY')
	current = scraper.network('eth').w3().eth.getBlock('latest')['number'] # Current block number
	deployed_at = 11809212 # Block Hoge was deployed at

	thread_pool = [Thread(target=get_address, args=(blocks, addrs, scraper, oLock)) for i in range(20)]

	for thread in thread_pool:
		thread.setDaemon(True)
		thread.start()		

	# Populate blocks Queue, 1000 block increments
	[blocks.put(i) for i in range(deployed_at, current, 1000)]

	blocks.join()

	addresses = set([addrs.get() for i in range(addrs.qsize())])
	#print(addresses)
	print("Found %d unique addresses holding Hoge" % len(addresses))

if __name__ == '__main__':
	main()