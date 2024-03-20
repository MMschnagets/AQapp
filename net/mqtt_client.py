import paho.mqtt.client as mqtt
from data import db


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


def on_sign_up(client, userdata, message):
    msg_str = message.payload.decode("utf-8")


def on_data_msg(client, userdata, payload, topic, topic_path):
    device_id = topic_path[2]
    pollutant = topic_path[3]
    dbmanager = db.DBManager()
    dbmanager.insert_values("DataStream", AQDeviceID=int(device_id),
                            Pollutant=pollutant, Value=float(payload))


def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    msg_str = message.payload.decode("utf-8")
    topic_path_list = message.topic.split('/')
    print(f'RECEIVED MSG: TOPIC = {message.topic} PAYLOAD = {msg_str}')
    if "airquality/sign" in message.topic:
        on_sign_up(client, userdata, message)
    elif "airquality/data" in message.topic:
        on_data_msg(client, userdata, msg_str, message.topic, topic_path_list)
    else:
        print(f"Topic with unknown naming template: payload = {message.payload.decode("utf-8")} from {message.topic}")
    topic_parts_list = message.topic.split("/")
    print(f'{topic_parts_list=}')
    if "airquality/sign" in message.topic:
        device_id = topic_parts_list[2]
        if device_id not in userdata["devices"].keys():
            userdata["devices"].update({device_id: {}})
        userdata["devices"][device_id].update({tmp_str[:tmp_str.find(" = "):]: tmp_str[tmp_str.find(" = ") + 3::]})
        check_list = ["ID", "NAME", "CITY", "COUNTRY", "COORDINATES"]
        check_value = 0
        for key in check_list:
            if key in userdata["devices"][device_id].keys():
                check_value += 1
        print(check_value)
        print(len(check_list))
        if check_value == len(check_list):
            dbmanager = db.DBManager()
            geo_str = userdata["devices"][device_id]["COORDINATES"]
            devices_from_db = dbmanager.get_values("AQDevices")
            if int(device_id) in [devices_from_db[i]["AQDeviceID"] for i in range(len(devices_from_db))]:
                cond_str = f'AQDeviceID = {device_id};'
                dbmanager.update_values("AQDevices", cond_str,
                                        Name=f'"{userdata["devices"][device_id]["NAME"]}"',
                                        City=f'"{userdata["devices"][device_id]["CITY"]}"',
                                        Country=f'"{userdata["devices"][device_id]["COUNTRY"]}"',
                                        Latitude=geo_str[1:geo_str.find(","):],
                                        Longitude=geo_str[geo_str.find(",") + 2:len(geo_str) - 1:],
                                        Status=f'"Active"')
                print(f"Device UPDATED: {userdata["devices"][device_id]}")
            else:
                dbmanager.insert_values("AQDevices", AQDeviceID=userdata["devices"][device_id]["ID"],
                                        Name=f'"{userdata["devices"][device_id]["NAME"]}"',
                                        City=f'"{userdata["devices"][device_id]["CITY"]}"',
                                        Country=f'"{userdata["devices"][device_id]["COUNTRY"]}"',
                                        Latitude=geo_str[1:geo_str.find(","):],
                                        Longitude=geo_str[geo_str.find(",") + 2:len(geo_str) - 1:],
                                        Status=f'"Active"')
                print(f"Device INSERTED: {userdata["devices"][device_id]}")
    elif "airquality/data" in message.topic:
        device_id = topic_parts_list[2]
        pollutant = topic_parts_list[3]
        if device_id not in userdata["data"].keys():
            userdata["data"].update({device_id: {pollutant: float(tmp_str)}})
        dbmanager = db.DBManager()
        dbmanager.insert_values("DataStream", AQDeviceID=int(device_id),
                                Pollutant=pollutant, Value=float(tmp_str))

    # We only want to process 10 messages
    elif len(userdata) >= 100000:
        client.unsubscribe("airquality/#")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe("airquality/#")  # subscribe to all AQ-related MQTT topics


def start(host, port=1883, keepalive=60):
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
