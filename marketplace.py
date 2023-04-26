"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock
import logging
import unittest

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s', filename='test.log', filemode='a')


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        # Every producer has a unique id. The IDs start from 0 and every time there is a new producer, the variable
        # below is incremented
        self.id_producer = 0
        self.id_cart = 0

        # Dictionary for the producers
        self.producers_dictionary = {}
        # producers = > {id1: [prod1, prod2, prod3], id2: [prod4, prod5, prod6]}

        # Dictionary for the consumers' carts
        self.carts_dictionary = {}
        #carts = > {id1: [[product1, id_producer1], [product2, id_producer2]],
                   #id2: [[product3, id_producer3], [product4, id_producer4]}

        self.lock_publish = Lock()
        self.lock_add_cart = Lock()


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        logging.info("Register producer attempt")
        
        with self.lock_add_cart:
            self.id_producer = self.id_producer + 1
            self.producers_dictionary[self.id_producer] = []

        logging.info("Register producer success: %d", self.id_producer)

        return self.id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # Only one producer can publish a product at a time
        self.lock_publish.acquire()

        published_products = self.producers_dictionary.get(producer_id)

        if len(published_products) < self.queue_size_per_producer:
            self.producers_dictionary.get(producer_id).append(product)
            self.lock_publish.release()
            return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.lock_add_cart:
            self.id_cart = self.id_cart + 1
            self.carts_dictionary[self.id_cart] = []
        return self.id_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # Find the ID of the producer responsible for the desired product
        found_product = False
        id_searched_producer = None

        # Just a single consumer can add product in a time
        self.lock_add_cart.acquire()

        for id_producer in self.producers_dictionary.keys():
            if found_product == True:
                break
            for prod in self.producers_dictionary.get(id_producer):
                if prod == product:
                    id_searched_producer = id_producer
                    found_product = True
                    break

        # If the desired product is found then it should be removed from its producer's list
        # and added to the customer's cart
        if found_product == True:
            self.producers_dictionary.get(id_searched_producer).remove(product)
            self.carts_dictionary.get(cart_id).append([product, id_searched_producer])

        # Free the lock for the consumer
        self.lock_add_cart.release()

        return found_product

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        list = self.carts_dictionary.get(cart_id)
        producer_id = None
        # Iterate the list to find the id for producer
        for prod, id in list:
            # Verify if we reached the desired product
            if prod == product:
                producer_id = id
                break
        # Remove product from cart
        list.remove([product, producer_id])
        self.carts_dictionary[cart_id] = list

        # Add the product back to its producer
        self.producers_dictionary.get(producer_id).append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        order = []
        for product, producer_id in self.carts_dictionary.get(cart_id):
            order.append(product)

        return order


class TestMarketplace(unittest.TestCase):

    def setUp(self):
        self.marketplace = Marketplace(5)


    def test_register_producer(self):
        producer_id = self.marketplace.register_producer()
        self.assertEqual(producer_id, 1)


    def test_publish(self):
        producer_id = self.marketplace.register_producer()
        product1 = "product1"
        product2 = "product2"
        self.assertTrue(self.marketplace.publish(producer_id, product1))
        self.assertTrue(self.marketplace.publish(producer_id, product2))
        self.assertFalse(self.marketplace.publish(producer_id, "product3"))


    def test_new_cart(self):
        cart_id = self.marketplace.new_cart()
        self.assertEqual(cart_id, 1)


    def test_add_to_cart(self):
        producer_id = self.marketplace.register_producer()
        product1 = "product1"
        product2 = "product2"
        self.marketplace.publish(producer_id, product1)
        self.marketplace.publish(producer_id, product2)
        cart_id = self.marketplace.new_cart()
        self.assertTrue(self.marketplace.add_to_cart(cart_id, product1))
        self.assertTrue(self.marketplace.add_to_cart(cart_id, product2))
        self.assertFalse(self.marketplace.add_to_cart(cart_id, "product3"))

    def test_remove_from_cart(self):
        producer_id = self.marketplace.register_producer()
        product1 = "product1"
        product2 = "product2"
        self.marketplace.publish(producer_id, product1)
        self.marketplace.publish(producer_id, product2)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product1)
        self.marketplace.add_to_cart(cart_id, product2)
        self.marketplace.remove_from_cart(cart_id, product1)
        self.assertEqual(self.marketplace.carts_dictionary[cart_id], [[product2, producer_id]])

    def test_place_order(self):
        producer_id = self.marketplace.register_producer()
        product1 = "product1"
        product2 = "product2"
        self.marketplace.publish(producer_id, product1)
        self.marketplace.publish(producer_id, product2)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, product1)
        self.marketplace.add_to_cart(cart_id, product2)
        order = self.marketplace.place_order(cart_id)
        self.assertEqual(order, [product1, product2])