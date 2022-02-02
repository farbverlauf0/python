def fib(n):
    if n == 0:
        return [0]
    result = [0, 1]
    for _ in range(2, n + 1):
        result.append(result[-2] + result[-1])
    return result
