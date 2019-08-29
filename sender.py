import time
import stomp
from xml_doc import XmlDoc

from rate_limit import RateLimited


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('received a message "%s"' % message)


conn = stomp.Connection(auto_content_length=False)
conn.set_listener('', MyListener())
conn.start()
conn.connect('admin', 'password', wait=True)
conn.subscribe(destination='/queue/test', id=1, ack='auto')


xml_doc = XmlDoc('EquityNew - Copy (1).xml')
print(xml_doc.event_id), exit()


@RateLimited(100)
def conn_send(body, destination):
    conn.send(body=body, destination=destination)


start_time = time.time()

for e in range(5000):
    conn_send(body=str(e), destination='/queue/test')

stop_time = time.time()

time.sleep(2)
print(stop_time - start_time)
conn.disconnect()




# if __name__ == '__main__':
#     while True:
#         time.sleep(5)
#         conn.send_life_sign()
