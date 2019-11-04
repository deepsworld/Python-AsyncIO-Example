import asyncio


async def myCoroutine():
    await asyncio.sleep(1)
    print("In the Coroutine")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(myCoroutine())
    loop.close()

if __name__ == '__main__':
    main()