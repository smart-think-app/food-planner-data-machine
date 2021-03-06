import json
import provider
from queue_module import switch_consumer

config = provider.get_config()
channel = provider.connection_rabbitmq(config)


def run_consumer(mq_channel_connect):
    mq_channel_connect.basic_qos(prefetch_count=1)
    with open("queue_consumer.json") as data_json_file:
        data = json.load(data_json_file)
        for item in data["Message"]:
            consumer_model = switch_consumer(item["QueueName"], mq_channel_connect)
            mq_channel_connect.basic_consume(queue=consumer_model.queue_name,
                                             on_message_callback=consumer_model.callback)
    print("Running Consumer....")
    mq_channel_connect.start_consuming()


run_consumer(channel)
