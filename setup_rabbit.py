import time
import urllib

import yaml
import requests
from requests.auth import HTTPBasicAuth

from config import Config

EXCHANGES_TO_IGNORE = ['', 'amq.direct', 'amq.fanout', 'amq.headers', 'amq.match', 'amq.rabbitmq.log',
                       'amq.rabbitmq.trace', 'amq.topic']


def gather_existing_config():
    return {'queues': gather_existing_queue_config(), 'exchanges': gather_existing_exchange_config(),
            'bindings': gather_existing_binding_config()}


def gather_existing_queue_config():
    existing_queues = []

    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    response = requests.get(f"{Config.RABBITMQ_API}/queues/{v_host}",
                            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()

    all_queues = response.json()

    for queue in all_queues:
        existing_queues.append({'name': queue['name'], 'arguments': queue.get('arguments') or {}})

    return existing_queues


def gather_existing_exchange_config():
    existing_exchanges = []

    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    response = requests.get(f"{Config.RABBITMQ_API}/exchanges/{v_host}",
                            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()

    all_exchanges = response.json()

    for exchange in all_exchanges:
        exchange_name = exchange['name']
        if exchange_name not in EXCHANGES_TO_IGNORE:
            existing_exchanges.append({'name': exchange_name, 'type': exchange['type']})

    return existing_exchanges


def gather_existing_binding_config():
    existing_bindings = []

    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    response = requests.get(f"{Config.RABBITMQ_API}/bindings/{v_host}",
                            auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
    response.raise_for_status()

    all_bindings = response.json()

    for binding in all_bindings:
        source_exchange = binding['source']
        if source_exchange != '':
            destination_queue = binding['destination']
            routing_key = binding['routing_key']
            existing_bindings.append({'sourceExchange': source_exchange, 'destinationQueue': destination_queue,
                                      'routingKey': routing_key})

    return existing_bindings


def create_exchanges(exchange_list, existing_exchange_list):
    for exchange in exchange_list:
        if not any(existing_exchange['name'] == exchange['name'] for existing_exchange in existing_exchange_list):
            create_exchange(exchange['name'], exchange['type'])
        else:
            print(f"Skipping exchange {exchange['name']} because it already exists")


def create_exchange(name, exchange_type):
    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    exchange_details = {"type": exchange_type, "auto_delete": False, "durable": True, "internal": False,
                        "arguments": {}}
    response = requests.put(f"{Config.RABBITMQ_API}/exchanges/{v_host}/{name}",
                            json=exchange_details, auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

    response.raise_for_status()


def create_queues(queue_list, existing_queue_list):
    for queue in queue_list:
        if not any(existing_queue['name'] == queue['name'] for existing_queue in existing_queue_list):
            create_queue(queue['name'], queue.get('arguments') or {})
        else:
            print(f"Skipping queue {queue['name']} because it already exists")


def create_queue(name, arguments):
    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    queue_details = {"auto_delete": False, "durable": True, "arguments": arguments}
    response = requests.put(f"{Config.RABBITMQ_API}/queues/{v_host}/{name}",
                            json=queue_details, auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

    response.raise_for_status()


def create_bindings(binding_list, existing_binding_list):
    for binding in binding_list:
        if not any(existing_binding['sourceExchange'] == binding['sourceExchange'] and
                   existing_binding['destinationQueue'] == binding['destinationQueue'] for existing_binding in
                   existing_binding_list):
            create_binding(binding['sourceExchange'], binding['destinationQueue'], binding.get('routingKey') or '')
        else:
            print(f"Skipping binding {binding['sourceExchange']} -> {binding['destinationQueue']} because it already "
                  "exists")


def create_binding(source_exchange, destination_queue, routing_key):
    v_host = urllib.parse.quote(Config.RABBITMQ_VHOST, safe='')

    binding_details = {"routing_key": routing_key, "arguments": {}}
    response = requests.post(f"{Config.RABBITMQ_API}/bindings/{v_host}/e/{source_exchange}/q/{destination_queue}",
                             json=binding_details, auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))

    response.raise_for_status()


def wait_for_rabbit():
    print('Waiting for Rabbit to start up...')
    while True:
        try:
            response = requests.get(f"{Config.RABBITMQ_API}/healthchecks/node",
                                    auth=HTTPBasicAuth(Config.RABBITMQ_USER, Config.RABBITMQ_PASSWORD))
            if response.status_code == 200:
                break
        except:
            pass

        time.sleep(1)


def main():
    wait_for_rabbit()

    existing_config = gather_existing_config()
    # Uncomment the line below to dump out the existing config as YAML
    # print(yaml.dump(existing_config))

    with open('rabbitmq/config.yml', 'r') as config_file:
        new_config = yaml.load(config_file, Loader=yaml.FullLoader)

        create_exchanges(new_config['exchanges'], existing_config['exchanges'])
        create_queues(new_config['queues'], existing_config['queues'])
        create_bindings(new_config['bindings'], existing_config['bindings'])


if __name__ == "__main__":
    main()
