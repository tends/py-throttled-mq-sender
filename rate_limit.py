import time


def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0] #[0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = lastTimeCalled[0]  # time.perf_counter() - lastTimeCalled[0]

            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            start__time = time.perf_counter()
            ret = func(*args,**kargs)
            stop__time = time.perf_counter()

            lastTimeCalled[0] = stop__time - start__time  #time.perf_counter()
            return ret
        return rateLimitedFunction
    return decorate