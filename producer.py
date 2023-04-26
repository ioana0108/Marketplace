"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs


    def run(self):
        while True:
            producer_id = self.marketplace.register_producer()
            for product in self.products:
                added_quantity = 0
                while added_quantity < product[1]:
                    wait = self.marketplace.publish(producer_id, product[0])
                    if wait == True:
                        added_quantity = added_quantity + 1
                        time.sleep(product[2])
                    else:
                        time.sleep(self.republish_wait_time)
