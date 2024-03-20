import time
from datetime import datetime


def meas_time(func):
    def wrapper(*args, **kwargs):
        time_before_sleep = datetime.now()
        result = func(*args, **kwargs)
        time_after_sleep = datetime.now()
        time_difference = time_after_sleep - time_before_sleep
        print(f'Time before sleep: {time_before_sleep},'
              f'time after sleep: {time_after_sleep},'
              f'calculated difference: {time_difference.total_seconds()}')
        return result
    return wrapper


class RandProc:
    value = 0

    def __init__(self):
        RandProc.value += 1
        self.number = RandProc.value
        self.creation_time = datetime.now()

    @meas_time
    def wait_time(self, seconds):
        time.sleep(seconds)

    def main(self):
        while True:
            print(self)
            self.wait_time(30)

    def __repr__(self):
        return f"{datetime.now()}| RandProc number = {self.number}, creation_time is {self.creation_time}"
