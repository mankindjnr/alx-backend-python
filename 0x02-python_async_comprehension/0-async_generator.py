#!/usr/bin/env python3
"""
a coroutine that takes no arguments
"""
from typing import Generator
import asyncio
import random


async def async_generator() -> Generator[float, None]:
    """
    the coroutine will loop 10 times and each time wait
    1 second and yield a num between 0 and 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield(random.uniform(0, 10))
