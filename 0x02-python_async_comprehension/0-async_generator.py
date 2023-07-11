#!/usr/bin/env python3
"""
a coroutine that takes no arguments
"""
from typing import List, AsyncGenerator
import asyncio
import random


async def async_generator() -> AsyncGenerator[float, None]:
    """
    the coroutine will loop 10 times and each time wait
    1 second and yield a num between 0 and 10
    """
    for _ in range(10):
        await asyncio.sleep(1)
        number: float = random.uniform(0, 10)
        yield(number)

