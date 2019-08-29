
import time
from ratelimit import limits, sleep_and_retry
import stomp


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('received a message "%s"' % message)


conn = stomp.Connection()
conn.set_listener('', MyListener())
conn.start()
conn.connect('admin', 'password', wait=True)

conn.subscribe(destination='/queue/test', id=1, ack='auto')

# conn.send(body=' '.join(sys.argv[1:]), destination='/queue/test')


def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.perf_counter() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.perf_counter()
            return ret
        return rateLimitedFunction
    return decorate

# @sleep_and_retry
# @limits(calls=20, period=1)
@RateLimited(20)
def conn_send(body, destination):
    conn.send(body=body, destination=destination)


start_time = time.time()

for e in range(100):
    conn_send(body=str(e), destination='/queue/test')

stop_time = time.time()
print(stop_time - start_time)
time.sleep(2)

conn.disconnect()




# if __name__ == '__main__':
#     while True:
#         time.sleep(5)
#         conn.send_life_sign()
