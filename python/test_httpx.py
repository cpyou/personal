import asyncio
import httpx
import threading
import time


async def async_main(url, sign):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        status_code = response.status_code
        print(f'async_main: {threading.current_thread()}: {sign}:{status_code}')


async def main():
    # Schedule three calls *concurrently*:
    async_start = time.time()
    tasks = [async_main(url='https://www.baidu.com', sign=i) for i in range(20)]
    l = await asyncio.gather(
        *tasks
    )
    print(l)
    async_end = time.time()
    print(async_end - async_start)


asyncio.run(main())
