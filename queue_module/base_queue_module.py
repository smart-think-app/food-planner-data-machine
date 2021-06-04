from abstract import AbstractConsumerModel
from enum_class import QueueNameEnum
from .init_food_planner_consumer import InitFoodPlannerConsumer
from provider import MQChannelManager


class DefaultConsumerModel(AbstractConsumerModel):
    def __init__(self, queue_name):
        self.queue_name = queue_name

    def callback(self, ch, method, properties, body):
        print("Default")
        print(" [x] Received %r" % body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)


def switch_consumer(queue_name, channel):
    if queue_name == QueueNameEnum.InitFoodPlanner.value:
        mq_manager = MQChannelManager(channel)
        return InitFoodPlannerConsumer(queue_name, mq_manager)
    return DefaultConsumerModel("")
