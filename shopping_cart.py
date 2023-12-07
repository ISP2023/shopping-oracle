"""Shopping Cart for recording items a customer wants to purchase.
   A Shopping Cart has a reference to the Store that products will be bought from.

   Requires Python 3.9 for type hints using built-in types.
"""
from decimal import Decimal
from store import Store, InventoryError
from config import *
import os


def bug(index: int) -> bool:
    TESTCASE = int(os.getenv('TESTCASE'))
    return index == TESTCASE

class ShoppingCart:
    """A class representing a shopping cart in an e-commerce application."""

    def __init__(self, store: Store) -> None:
        """Initialize an empty shopping cart.

           :param store: the Store that this shopping cart gets products from.
        """
        self.cart: dict[int, int] = {}    # product_id -> quantity
        self.store = store

    def add_item(self, product_id: int, quantity: int) -> None:
        """
        Add the specified quantity of a product to the shopping cart.
        If the product_id is already in the shopping cart, then the quantity is increased.

        :param product_id: The ID of the product to be added.
        :param quantity: The quantity of the product to be added.

        :raises ValueError: If the product ID is not a known product,
                            the quantity is not positive, or
                            the quantity would cause the total quantity in the
                            shopping cart to exceed the stock in the store.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be positive integer")
        if bug(ADD_NONEXISTENT_PRODUCT):
            stock = 2**30
        else:
            # will raise exception if product_id not in store
            stock = self.store.get_quantity(product_id)
        if bug(BYPASS_STOCK_LIMIT):
            # only check _this_ quantity is in stock
            total_quantity = quantity
        else:
            # total in cart + new quantity in stock?
            total_quantity = self.cart.get(product_id, 0) + quantity
        if total_quantity > stock:
            raise ValueError(f"Quantity {total_quantity} exceeds stock of {product_id}")
        self.cart[product_id] = self.cart.get(product_id, 0) + quantity

    def remove_item(self, product_id: int, quantity: int) -> None:
        """
        Remove the specified quantity of a product from the shopping cart.

        If the quantity of product_id is reduced to zero,
        then remove the product from the cart.

        :param product_id: The ID of the product to update quantity.
        :param quantity: The amount of the product to be removed, must be positive.

        :raises ValueError: If the product ID is not a product in the shopping cart,
                the quantity is not positive, or the quantity exceeds the quantity
                of this product in the shopping cart.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be positive integer")
        if not product_id in self.cart:
            raise ValueError(f"{product_id} is not the ID of a Product in shopping cart")
        qnty_in_cart = self.cart[product_id]
        if quantity > qnty_in_cart and not bug(REMOVE_QUANTITY_EXCEEDS_CART):
            raise ValueError(
                f"Quantity {quantity} exceeds quantity {qnty_in_cart} of {product_id} in cart")
        # Reduce the quantity in cart. 
        self.cart[product_id] -= quantity
        # If remaining quantity is 0 then remove item from cart.
        if self.cart[product_id] == 0:
            del self.cart[product_id]

    def get_items(self) -> dict[int, int]:
        """Return a dictionary of the items in the cart.

        :return: dict of items in the cart. Keys are product id and values are quantity.
        The return value is a copy, and not updated if the cart contents change later.
        Example:
        > cart.add_item(123, 7)
        > cart.get_items()
        {123: 7}
        """
        return self.cart.copy()

    def get_quantity(self, product_id: int) -> int:
        """Get the quantity of an item in the shopping cart for a product_id.

        :param product_id: the prodoct ID of the item to get
        :return: the quantity of an item in the cart, or 0 if item is not in the cart.
        """
        return self.cart.get(product_id, 0)

    def get_total_price(self) -> Decimal:
        """
        Return the total price of all items in the shopping cart.
        No check is done as to whether the Store still has sufficient stock
        to supply the quantity of each item in the cart (checkout checks that).

        :return: The total price of all items in the shopping cart, as a Decimal.

        :raises ValueError: If the product_id of any item in the cart
            is not found in the store. This can happen if a product is
            deleted from the store after it is added to the cart.
        """
        total = Decimal('0')
        for (product_id, quantity) in self.cart.items():
            try:
                product = self.store.get_product(product_id)
                product_price = product.price
            except ValueError as ex:
                if bug(ADD_NONEXISTENT_PRODUCT):
                    product_price = 0
                else:
                    raise ex
            total += product_price * quantity
        return total

    def checkout(self) -> str:
        """
        Complete the checkout process, update quantities of items in the store,
        and then clear the shopping cart.  If any updates fail then nothing
        is changed (store's inventory not changed and shopping cart is not cleared).

        :return: a unique string order identifier supplied by the store
        :raises InventoryError: If the checkout cannot be completed due to insufficient
            inventory of any items in the shopping cart.
        :raises ValueError: if some product_id in the cart is not a current Product
        """
        if not bug(CHECKOUT_CORRUPTS_INVENTORY):
            # verify stock quantities before updating inventory (correct)
            for (product_id, quantity) in self.cart.items():
                qnty_in_stock = self.store.get_quantity(product_id)
                if quantity > qnty_in_stock:
                    # exceeds inventory
                    raise InventoryError(
                        f"Product {product_id} in-stock {qnty_in_stock} < in-cart {quantity}")
            # update the store's inventory
            if not bug(CHECKOUT_DOES_NOT_UPDATE_INVENTORY):
                for (product_id, quantity) in self.cart.items():
                    self.store.add_stock(product_id, -quantity)

        # if no exceptions raised, then place the order
        order_id = self.store.place_order(self.cart)
        # after placing an order, empty the cart to avoid duplicate orders
        if order_id and not bug(CHECKOUT_NOT_EMPTY_CART):
            self.cart.clear()
        return order_id
