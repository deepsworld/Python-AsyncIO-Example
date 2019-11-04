import asyncio
import random

# Python Async Code
async def myCoroutine(id):
    process_time = random.randint(1,5)
    await asyncio.sleep(process_time)

    print(f'Coroutine {id} took {process_time} sec to complete')
import time
async def main():
    t = time.time()
    tasks = []
    for _ in range(10):
        tasks.append(asyncio.ensure_future(myCoroutine(_)))

    await asyncio.gather(*tasks)
    print(time.time() - t)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()


# Regular Syncronous Code
def mCoroutine(id):
    process_time = random.randint(1,5)
    time.sleep(process_time)
    print(f'Coroutine {id} took {process_time} sec to complete')

def main():
    t = time.time()
    tasks = []
    for _ in range(10):
        mCoroutine(_)

    print(time.time() - t)

main()