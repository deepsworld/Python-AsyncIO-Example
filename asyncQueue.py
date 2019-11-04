import asyncio

async def consumer(Q):
    return await Q.get() # gets from the Queue - Blocking but async

def producer(Q, item):
    Q.put_nowait(item) # Puts to the Queue without blocking

async def main():
    a = asyncio.Queue()

    producer(a, "Bro")
    r = await consumer(a)
    print(r)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
finally:
    loop.close()