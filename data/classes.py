class Device:
    def __init__(self, dev_id: int, name: str):
        self.dev_id = dev_id
        self.name = name


class GeoData:
    def __init__(self, dev_id: int, city: str, country: str, latitude: float, longitude: float):
        self.dev_id = dev_id
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude


class RawData:
    def __init__(self, dev_id: int, pm25: float, pm10: float, o3: float, no2: float, so2: float, co: float,
                 save_time: str = None):
        self.dev_id = dev_id
        self.pm25 = pm25
        self.pm10 = pm10
        self.o3 = o3
        self.no2 = no2
        self.so2 = so2
        self.co = co
        self.save_time = save_time
