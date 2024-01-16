#!/usr/bin/env python3
""" task wait random"""
import asyncio

wait_n = __import__('1-concurrent_coroutines').wait_n


async def task_wait_n(n: int, max_delay: int) -> asyncio.Task:
    """ spawn wait_random with the specified max_delay."""
    return await asyncio.create_task(wait_n(n, max_delay))
