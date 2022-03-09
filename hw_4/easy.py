import time
from threading import Thread
from multiprocessing import Process


def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


if __name__ == '__main__':
    d = {}

    # Normal
    start = time.time()
    for _ in range(10):
        fib(500000)
    duration = time.time() - start
    d['sync'] = duration

    # Threads
    start = time.time()
    threads = []
    for _ in range(10):
        t = Thread(target=fib, args=(500000, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    duration = time.time() - start
    d['threads'] = duration

    # Processes
    start = time.time()
    procs = []
    for _ in range(10):
        p = Process(target=fib, args=(500000, ))
        procs.append(p)
        p.start()
    for p in procs:
        p.join()
    duration = time.time() - start
    d['processes'] = duration

    with open('easy_artifact.txt', 'w') as f:
        for key, value in d.items():
            f.write(f'Time ({key}): {value}s\n')
