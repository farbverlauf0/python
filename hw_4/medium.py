import math
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from datetime import datetime

def sync_integrate(f, a, b, n_iter):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc

def sync_integrate_with_log(args):
    f, a, b, n_iter, i, n_jobs = args
    sync_integrate_with_log.buffer += f'{i + 1}th job was executed at {datetime.now()} with n_jobs={n_jobs}\n'
    return sync_integrate(f, a, b, n_iter)

sync_integrate_with_log.buffer = ''

def integrate(f, a, b, *, n_jobs=1, n_iter=1000):
    step = (b - a) / n_jobs
    args = [(f, a + i * step, a + (i + 1) * step, n_iter // n_jobs, i, n_jobs) for i in range(n_jobs)]
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        result = sum(executor.map(sync_integrate_with_log, args))
    with open('medium_log.txt', 'a') as f:
        f.write(sync_integrate_with_log.buffer)
    sync_integrate_with_log.buffer = ''
    return result

if __name__ == '__main__':
    cpu_count, n_iter = cpu_count(), 5 * 10 ** 8

    # Normal
    start = time.time()
    res = sync_integrate(math.cos, 0, math.pi/2, n_iter)
    message = f'Sync calc executed in {time.time() - start}, res={res}\n'
    print(message, end='')
    with open('compare.txt', 'a') as f:
        f.write(message)

    # On multiple cpu
    for n_jobs in range(1, 2 * cpu_count + 1):
        start = time.time()
        res = integrate(math.cos, 0, math.pi/2, n_jobs=n_jobs, n_iter=n_iter)
        message = f'Processpool with n_jobs={n_jobs} executed in {time.time() - start}, res={res}\n'
        print(message, end='')
        with open('compare.txt', 'a') as f:
            f.write(message)
