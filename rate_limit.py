import time


def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)

    def decorate(func):
        elapsed = [0]  # [0.0]

        def rateLimitedFunction(*args, **kargs):
            leftToWait = minInterval - elapsed[0]
            if leftToWait > 0:
                time.sleep(leftToWait)
            start__time = time.perf_counter()
            ret = func(*args, **kargs)
            stop__time = time.perf_counter()

            elapsed[0] = stop__time - start__time
            return ret

        return rateLimitedFunction

    return decorate
