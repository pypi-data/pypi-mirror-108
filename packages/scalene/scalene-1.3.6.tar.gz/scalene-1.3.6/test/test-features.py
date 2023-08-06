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

@profile
def t1_sleep():
    if False:
        url = 'https://github.com/plasma-umass/scalene'
        r = requests.get(url, allow_redirects=True)
        s = r.text
        for i in range(8):
            s = s + ":" + s
        print(len(s))
        for i in range(100):
            with tempfile.TemporaryFile(mode='w') as f:
                f.write(s)
        print("wrote")
    print("sleeping.")
    time.sleep(2)
    print("done sleeping.")

its = 10000000

@profile
def t2_seq_python():
    x = []
    for i in range(its):
        x.append(i)

@profile
def t2_thread():
    x = []
    for i in range(5 * its):
        x.append(i)
        
@profile
def t_thread():
    t = threading.Thread(target=t2_thread)
    return t

@profile
async def t4_async():
    x = []
    for i in range(its):
        x.append(i)
    await asyncio.sleep(1)

@profile
async def main():
  t = t_thread()
  t.start()
  t1_sleep()
  t2_seq_python()
  await t4_async()
  t.join()

def sleepy():
    time.sleep(3)
    
if __name__ == '__main__':
    asyncio.run(main())
    sleepy()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
