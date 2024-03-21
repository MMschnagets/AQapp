CREATE_TABLE = {
    'devices': 'CREATE TABLE IF NOT EXISTS devices ('
    'dev_id INTEGER PRIMARY KEY,'
    'name TEXT NOT NULL);',
    'geo_data': 'CREATE TABLE IF NOT EXISTS geo_data ('
    'dev_id INTEGER PRIMARY KEY,'
    'city TEXT NOT NULL,'
    'country TEXT NOT NULL,'
    'latitude FLOAT NOT NULL,'
    'longitude FLOAT NOT NULL,'
    'FOREIGN KEY (dev_id) REFERENCES devices(dev_id));',
    'raw_data': 'CREATE TABLE IF NOT EXISTS raw_data ('
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
INSERT_VALUE = {
    'devices': 'INSERT INTO devices (dev_id, name) VALUES (?, ?);',
    'geo_data': 'INSERT INTO geo_data (dev_id, city, country, latitude, longitude) VALUES (?, ?, ?, ?, ?);',
    'raw_data': 'INSERT INTO raw_data (dev_id, pm25, pm10, o3, no2, so2, co) VALUES (?, ?, ?, ?, ?, ?, ?);'
}
SELECT_VALUE = {
    'devices': {
        'all': 'SELECT * FROM devices',
        'only_id': 'SELECT dev_id FROM devices',
        'dev_id': 'SELECT name FROM devices WHERE dev_id = ?;'
    },
    'geo_data': {
        'all': 'SELECT * FROM geo_data',
        'coordinates': 'SELECT (latitude, longitude) FROM geo_data WHERE dev_id = ?;',
        'dev_id': 'SELECT (city, country, latitude, longitude) FROM geo_data WHERE dev_id = ?;'
    },
    'raw_data': {
        'all': 'SELECT * FROM raw_data',
        'pollutants': 'SELECT (pm25, pm10, o3, no2, so2, co) FROM raw_data WHERE dev_id = ?;',
        'dev_id': 'SELECT (pm25, pm10, o3, no2, so2, co, save_time) FROM raw_data WHERE dev_id = ?;'
    },
},
UPDATE_VALUE = {
    'devices': {
        'all': 'UPDATE devices SET name = ? WHERE dev_id = ?;'
        },
    'geo_data': {
        'all': 'UPDATE geo_data SET city = ?, country = ?, latitude = ?, longitude = ? WHERE dev_id = ?;',
        'city_country': 'UPDATE geo_data SET city = ?, country = ? WHERE dev_id = ?;',
        'coordinates': 'UPDATE geo_data SET latitude = ?, longitude = ? WHERE dev_id = ?;'
    },
    'raw_data': {
        'all': 'UPDATE raw_data SET pm25 = ?, pm10 = ?, o3 = ?, no2 = ?, so2 = ?, co = ? WHERE dev_id = ?;',
        'pms': 'UPDATE raw_data SET pm25 = ?, pm10 = ? WHERE dev_id = ?;',
        'dev_id': 'UPDATE raw_data SET o3 = ?, no2 = ?, so2 = ?, co = ? WHERE dev_id = ?;'
    }
}