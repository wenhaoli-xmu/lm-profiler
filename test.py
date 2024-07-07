from profiler import WallTime
import time
import random


wt = WallTime('test')


for _ in range(10):
    with WallTime.get('test'):
        time.sleep(random.random())
    
wt.result(detail=True)