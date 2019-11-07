import paho.mqtt.client as mqtt
import threading
import time
import queue


class LocalClient(threading.Thread):

    def __init__(self, client_id='cloud_connector', host='localhost', port=1883):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.client_id = client_id
        self.subscription_paths = ['memory', 'loads', 'storage', 'people']
        self.message_queue = queue.Queue()
        self.client = mqtt.Client(client_id=self.client_id)

    def on_message(self, client, obj, msg):
        self.message_queue.put(msg)

    def subscribe_all(self, subscription_paths=None, qos=1):
        if subscription_paths is None:
            subscription_paths = []
        for path in subscription_paths:
            print('[MQTT_CLIENT] subscribe to ' + path)
            self.client.subscribe(path, qos=qos)
            time.sleep(0.5)

    def run(self) -> None:
        print('[MQTT_CLIENT] connecting to mqtt')
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.subscribe_all(self.subscription_paths)
        self.client.loop_forever()
