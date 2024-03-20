import threading
from utils import rand_proc
from net import mqtt_client

rp = rand_proc.RandProc()  # TODO: RANDOM PROCESS -> useful_feature_process_name (TASK_ID)
thread_1 = threading.Thread(target=mqtt_client.start, args=("127.0.0.1",))  # MQTT Client (subscriber) thread
thread_2 = threading.Thread(target=rp.main)  # TODO: RANDOM PROCESS -> useful_feature_process_name (TASK_ID)
thread_1.start()  # starting MQTT Client (subscriber) thread for receiving device's measured data
thread_2.start()  # TODO: RANDOM PROCESS -> useful_feature_process_name (TASK_ID)
