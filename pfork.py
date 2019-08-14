import os
import sys
import random
import time
from typing import Tuple

def some_work() -> int:
    wait_time: int = random.SystemRandom().randint(10, 20)
    pid: int = os.getpid()

    print('Child process works for %d sec (PID:%s)' % (wait_time, pid))
    time.sleep(wait_time)

    return wait_time

if __name__ == '__main__':
    for i in range(5):
        pid: int = os.fork()
        if pid == 0 : # No pid. so this is child process!
            result: int = some_work()
            child_pid: int = os.getpid()
            print('Child process worked for %d sec. (PID:%s)' % (result, child_pid))
            sys.exit()

    print('Ended main process (PID: %s)' % os.getpid())
