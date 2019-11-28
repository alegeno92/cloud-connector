import json
import sys
from Adafruit_IO import Client, RequestError, Feed, ThrottlingError
from local_client import LocalClient
from mock_local_client import MockLocalClient


def generate_feeds(aio, feeds_name):
    feeds = dict()
    for name in feeds_name:
        print('[AIO_REMOTE] generating ' + name + ' feed')
        try:
            feed = aio.feeds(name)
        except RequestError:
            feed = Feed(name=name)
            feed = aio.create_feed(feed)
        feeds[name] = feed
    return feeds


def read_configuration(path):
    print(path)
    with open(path) as json_data_file:
        data = json.load(json_data_file)
        print('[MAIN] reading configuration ok')
        return data


def main(configuration):
    aio = Client(configuration['AIO']['username'], configuration['AIO']['key'])
    topic_data_mapper = {feed['topic']: feed['data'] for feed in configuration['feeds']}
    feeds = generate_feeds(aio, topic_data_mapper.keys())
    if configuration['mock_client']:
        local_client = MockLocalClient()
    else:
        local_client = LocalClient(client_id=configuration['local']['client_id'],
                                   host=configuration['local']['host'],
                                   port=configuration['local']['port'],
                                   subscription_paths=topic_data_mapper.keys())
    local_client.start()
    while True:
        message = local_client.message_queue.get()

        if message is None:
            continue
        topic = message.topic
        payload = message.payload
        json_payload = json.loads(payload)
        print('[MAIN] received ' + str(topic) + ' ' + str(json_payload))
        feed = feeds[topic]
        try:
            if topic in topic_data_mapper.keys():
                aio.send_data(feed.key, json_payload['data'][topic_data_mapper[topic]])
                print('[AIO_REMOTE] send ' + str(topic) + ': ' + str(json_payload['data'][topic_data_mapper[topic]]))
            else:
                print('[AIO_REMOTE] discard message ' + str(topic) + str(json_payload))
        except ThrottlingError as e:
            print('[MAIN] Skipping value. Limit reached.')
            continue


if __name__ == "__main__":
    config_file = None
    if len(sys.argv) < 2:
        print("[MAIN] Usage: python3 main.py [config-file-path.json]")
        exit(1)
    else:
        config_file = sys.argv[1]
    config = read_configuration(config_file)
    main(config)
