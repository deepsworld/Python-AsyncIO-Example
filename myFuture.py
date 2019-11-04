import asyncio

# Define a coroutine that takes in a future
async def myCoroutine(future):
    await asyncio.sleep(1)

    future.set_result("Coroutine tuned future is complete")
    
async def main():
    future = asyncio.Future()

    await asyncio.ensure_future(myCoroutine(future))

    print(future.result())

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
finally:
    loop.close()