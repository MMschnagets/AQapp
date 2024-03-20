import threading
from utils import rand_proc
from net import mqtt_client

rp = rand_proc.RandProc() # TODO: Change random process instance to useful feature process
thread_1 = threading.Thread(target=mqtt_client.start, args=("127.0.0.1",))
thread_2 = threading.Thread(target=rp.main)
# thread_3 = threading.Thread(target=rp.main)
thread_1.start()
thread_2.start()
# thread_3.start()
