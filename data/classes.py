from db import DBManager


class Device:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def set_device_id(self, device_id):
        self.device_id = device_id
