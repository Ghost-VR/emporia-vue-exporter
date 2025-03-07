#!/usr/bin/env python3
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

async def main():
  # Logger
  logging.basicConfig(level=logging.INFO)

  _LOGGER.info("Whats up")

  await asyncio.sleep(2)

  _LOGGER.info("Yeet")


if __name__ == '__main__':
  asyncio.run(main())
