import paho.mqtt.client as mqtt
from data import db
from data.classes import Device


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")


def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()


def register_sensor(msg_data, sensor_id):
    select_result = db.select_values("devices", "name", " WHERE dev_id = ?", sensor_id)
    print(f'Selected result: {select_result}')
    if not select_result:
        db.insert_values("devices", (sensor_id, msg_data["name"]))
        db.insert_values("geo_data", (sensor_id, msg_data["city"], msg_data["country"],
                                      msg_data["latitude"], msg_data["longitude"]))


def on_data_msg(msg_data, device_id):
    select_result = db.select_values("raw_data", "dev_id", " WHERE dev_id = ?", device_id)
    msg_data.update({"dev_id": device_id})
    if not select_result:
        db.insert_values("raw_data", (msg_data["dev_id"], msg_data["pm25"], msg_data["pm10"],
                                      msg_data["o3"], msg_data["no2"], msg_data["so2"], msg_data["co"]))
        print(f'ON DATA MSG: {msg_data=}')
    else:
        db.update_values("raw_data", "all", (msg_data["pm25"], msg_data["pm10"],
                                             msg_data["o3"], msg_data["no2"], msg_data["so2"], msg_data["co"],
                                             msg_data["dev_id"]))


def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    msg_str = message.payload.decode("utf-8")
    print(f'RECEIVED MESSAGE | Topic: {message.topic} | Payload: {msg_str}')
    msg_pairs = msg_str.split(';')
    msg_list = [pair.split('=') for pair in msg_pairs]
    msg_data = {pair[0]: pair[1] for pair in msg_list}
    topic_path_list = message.topic.split('/')
    if "airquality/sign" in message.topic:
        msg_data.update({"latitude": msg_data['coordinates'][1:msg_data['coordinates'].find(", "):],
                         "longitude": msg_data['coordinates'][msg_data['coordinates'].find(", ") + 2:-1:]})
        register_sensor(msg_data, topic_path_list[2])
    elif "airquality/data" in message.topic:
        on_data_msg(msg_data, topic_path_list[2])
    else:
        print(f"Topic with unknown naming template: payload = {message.payload.decode("utf-8")} from {message.topic}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("airquality/#")  # subscribe to all AQ-related MQTT topics


def start(host, port=1883, keepalive=60):
    db_obj = db.DBWorker()
    db_obj_conn = db_obj.get_db_connection()
    for table_name in ['devices', 'geo_data', 'raw_data']:
        db.create_table(table_name)
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    user_data_dict = {"devices": {},
                      "data": {}}
    mqttc.user_data_set(user_data_dict)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    mqttc.connect(host, port, keepalive)
    mqttc.loop_forever()
