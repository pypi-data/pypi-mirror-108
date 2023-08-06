# Disable the @profile decorator if none has been declared.

try:
    # Python 2
    import __builtin__ as builtins
except ImportError:
    # Python 3
    import builtins

try:
    builtins.profile
except AttributeError:
    # No line profiler, provide a pass-through version
    def profile(func): return func
    builtins.profile = profile

import asyncio
import tempfile
import threading
import time
import os
import requests

its = 10000

@profile
async def t4_async():
    x = []
    for i in range(its):
        x.append(i)
    # await asyncio.sleep(0.01)

@profile
async def main():
  stmts = []
  for i in range(1000):
      stmts.append(t4_async())
  await asyncio.gather(*stmts)

if __name__ == '__main__':
    asyncio.run(main())
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
