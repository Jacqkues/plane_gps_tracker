import threading
from event_kafka_to_postgresql import start as event_start
from gps_kafka_to_postgresql import start as gps_start


thread1 = threading.Thread(target=gps_start)
thread2 = threading.Thread(target=event_start)

thread1.start()
thread2.start()

thread1.join()
thread2.join()