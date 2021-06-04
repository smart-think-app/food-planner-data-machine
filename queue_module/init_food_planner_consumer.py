import json
from enum_class import QueueNameEnum

from abstract import AbstractConsumerModel


class InitFoodPlannerConsumer(AbstractConsumerModel):

    def __init__(self, queue_name, mq_manager):
        self.queue_name = queue_name
        self.mq_manager = mq_manager

    def callback(self, ch, method, properties, body):
        try:
            data_init = json.loads(body.decode())
            food_planner = {
                "user_id": data_init["user_id"],
                "water_lit": 2.5,
                "diet": [
                    {
                        "date": "monday",
                        "meal": [
                            {
                                "name": "lunch",
                                "food": [
                                    {
                                        "food_id": 2,
                                        "name": "Beef",
                                        "image": "",
                                    },
                                    {
                                        "food_id": 3,
                                        "name": "Chicken",
                                        "image": "",
                                    }
                                ]
                            },
                            {
                                "name": "dinner",
                                "food": [
                                    {
                                        "food_id": 2,
                                        "name": "Beef",
                                        "image": "",
                                    },
                                    {
                                        "food_id": 3,
                                        "name": "Chicken",
                                        "image": "",
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "date": "tuesday",
                        "meal": [
                            {
                                "name": "lunch",
                                "food": [
                                    {
                                        "food_id": 2,
                                        "name": "Beef",
                                        "image": "",
                                    },
                                    {
                                        "food_id": 3,
                                        "name": "Chicken",
                                        "image": "",
                                    }
                                ]
                            },
                            {
                                "name": "dinner",
                                "food": [
                                    {
                                        "food_id": 2,
                                        "name": "Beef",
                                        "image": "",
                                    },
                                    {
                                        "food_id": 3,
                                        "name": "Chicken",
                                        "image": "",
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
            self.mq_manager.publish_message(QueueNameEnum.InsertUserPlanner.value, food_planner)
        except Exception as e:
            print(e)
        ch.basic_ack(delivery_tag=method.delivery_tag)
