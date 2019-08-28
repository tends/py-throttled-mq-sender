from amqstompclient import amqstompclient
import logging
import time
import stomp

stomp.Connection10

def callback(destination, message, headers):
    logger.info("Received:" + message)
    conn.send_message("/topic/TTEST2", "FROMCALLBACK")


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()

server = {"ip": "127.0.0.1", "port": "61613", "login": "admin", "password": "admin", "heartbeats": (30000, 30000)}
conn = amqstompclient.AMQClient(server
                                , {"name": "TEST", "version": "1.0.0", "lifesign": "/topic/HELLO"}
                                , ["/queue/QTEST1", "/queue/QTEST2", "/topic/HELLO"]
                                , callback=callback)

conn.send_message("/topic/COUCOU", "WUT!!!")

if __name__ == '__main__':
    while True:
        time.sleep(5)
        conn.send_life_sign()
