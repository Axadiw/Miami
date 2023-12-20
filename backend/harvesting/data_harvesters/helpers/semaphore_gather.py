import asyncio


async def semaphore_gather(num, coroutines, return_exceptions=False):
    semaphore = asyncio.Semaphore(num)

    async def _wrap_coro(coro):
        async with semaphore:
            return await coro

    return await asyncio.gather(*(_wrap_coro(coro) for coro in coroutines), return_exceptions=return_exceptions)
