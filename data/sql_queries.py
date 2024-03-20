CREATE_TABLE = {
    "devices": 'CREATE TABLE IF NOT EXISTS devices ('
    'dev_id INTEGER PRIMARY KEY,'
    'name TEXT NOT NULL);',
    "geo_data": 'CREATE TABLE IF NOT EXISTS geo_data ('
    'dev_id INTEGER PRIMARY KEY,'
    'city TEXT NOT NULL,'
    'country TEXT NOT NULL,'
    'latitude FLOAT NOT NULL,'
    'longitude FLOAT NOT NULL,'
    'FOREIGN KEY (dev_id) REFERENCES devices(dev_id));',
    "raw_data": 'CREATE TABLE IF NOT EXISTS raw_data ('
    'dev_id INTEGER PRIMARY KEY,'
    'pm25 FLOAT,'
    'pm10 FLOAT,'
    'o3 FLOAT,'
    'no2 FLOAT,'
    'so2 FLOAT,'
    'co FLOAT,'
    'save_time DATETIME DEFAULT CURRENT_TIMESTAMP,'
    'FOREIGN KEY (dev_id) REFERENCES devices(dev_id));'
}
