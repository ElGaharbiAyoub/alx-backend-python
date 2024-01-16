#!/usr/bin/env python3
""" task wait random"""
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """ spawn wait_random with the specified max_delay."""
    return asyncio.create_task(wait_random(max_delay))
