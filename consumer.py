"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        # self.name = kwargs['name']
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs


    def print_cart(self, id_cart):
        list_order = self.marketplace.place_order(id_cart)
        for product in list_order:
            print(self.name, "bought", product)

    def run(self):
        for cart_items in self.carts:
            # We need to initialize the cart in question
            cart_id = self.marketplace.new_cart()
            for item in cart_items:
                item_type = item.get("type")
                item_id = item.get("product")
                item_quantity = item.get("quantity")

                if item_type == "add":
                    added_quantity = 0
                    # Add products in the quantity resulted from json
                    while added_quantity < item_quantity:
                        wait = self.marketplace.add_to_cart(cart_id, item_id)
                        if wait:
                            added_quantity = added_quantity + 1
                        else:
                            time.sleep(self.retry_wait_time)
                else:
                    removed_quantity = 0
                    while removed_quantity < item_quantity:
                        self.marketplace.remove_from_cart(cart_id, item_id)
                        removed_quantity += 1
            self.print_cart(cart_id)
