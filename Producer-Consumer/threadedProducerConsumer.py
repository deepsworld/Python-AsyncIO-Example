import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
 
import requests
 
queue = asyncio.Queue()
 
 
"""
Producer, simplely takes the urls and dump them into the queue
"""
async def produce(queue):
    inputf = ['https://google.com', 'https://yahoo.com', 'https://cnn.com']
    for url in inputf:
        await queue.put(url)
 
    await queue.put(None) # poison pill to signal all the work is done
 
"""
Helper function to send request and manipulate response
"""
async def async_request(url, loop, callback=None):
    print("Sending request to: " + url)
    """
    This is a canonical way to turn a synchronized routine to async. event_loop.run_in_executor, 
    by default, takes a new thread from ThreadPool. 
    It is also possible to change the executor to ProcessPool.
    """
    ret = await loop.run_in_executor(ThreadPoolExecutor(), partial(requests.get, timeout=5), url)
    if callback is not None:
        callback(url, ret.text)
 
 
"""
Consumer with an infinite loop. It only stops if there is a poison pill.
"""
async def consume(queue, loop):
    with open('output.txt', 'w', encoding='utf-8') as f:
 
        def write_to_file(url, ret):
            f.write(url + "|" + ret + "\n")
 
        while True:
            item = await queue.get() # coroutine will be blocked if queue is empty
 
            if item is None: # if poison pill is detected, exit the loop
                break
 
            await async_request(item, loop, write_to_file)
            # signal that the current task from the queue is done 
            # and decrease the queue counter by one
            queue.task_done() 
 
"""
Driver
"""
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    producer_coro = produce(queue)
    consumer_coro = consume(queue, loop)
    loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
    loop.close()