import queue
import threading
import time
import paho.mqtt.client as mqtt

import json
import random


def mock_memory_message():
    message = mqtt.MQTTMessage()
    message.topic = b"memory"
    message.payload = bytes(json.dumps({
        "data": {
            "value": random.randint(0, 100)
        }
    }), encoding='utf8')

    return message


def mock_loads_message():
    message = mqtt.MQTTMessage()
    message.topic = b"loads"
    message.payload = bytes(json.dumps({
        "data": {
            "value": random.randint(0, 100)
        }
    }), encoding='utf8')
    return message


def mock_storage_message():
    message = mqtt.MQTTMessage()
    message.topic = b"storage"
    message.payload = bytes(json.dumps({
        "data": {
            "value": random.randint(0, 100)
        }
    }), encoding='utf8')
    return message


def mock_people_message():
    message = mqtt.MQTTMessage()
    message.topic = b"people"
    message.payload = bytes(json.dumps({
        "data": {
            "value": random.randint(0, 100)
        }
    }), encoding='utf8')

    return message


class MockLocalClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.message_queue = queue.Queue()

    def run(self):
        while True:
            rnd = random.randint(0, 3)
            if rnd == 0:
                message = mock_memory_message()
            elif rnd == 1:
                message = mock_loads_message()
            elif rnd == 2:
                message = mock_storage_message()
            else:
                message = mock_people_message()

            self.message_queue.put(message)

            time.sleep(5)
