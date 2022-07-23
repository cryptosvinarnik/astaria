import aiohttp
import asyncio

from loguru import logger


url = "https://xyz.us11.list-manage.com/subscribe/" \
      "post-json?u=7ba25d0a2461b4e360ab05a54&amp;" \
      "id=9c1bff8a37&EMAIL={}&c=__jp0"


async def subscribe_on_solana(worker: str, queue: asyncio.Queue) -> None:
    i = 0

    while not queue.empty():
        email = await queue.get()

        async with aiohttp.ClientSession() as session:
            async with session.get(url.format(email.split(":")[0])) as resp:
                if "Thank" in await resp.text():
                    logger.success(
                        f"{worker} - {email} successfully registered")
                else:
                    logger.error(f"{worker} - {email} - error!")

        i += 1

        if i % 4 == 0:
            logger.info(f"{worker} - Sleeping 60 seconds...")
            await asyncio.sleep(60)


async def main(emails):
    queue = asyncio.Queue()

    for email in emails:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(subscribe_on_solana(
             f"Worker {i}", queue)) for i in range(5)]

    await asyncio.gather(*tasks)