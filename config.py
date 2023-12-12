"""Configuration for instrumented target code."""
import os

# cart only checks if incremental quantity added <= stock, not total in cart
BYPASS_STOCK_LIMIT = 1
# can add product id of non-existing product to cart
ADD_NONEXISTENT_PRODUCT = 2
# can add zero quantity of an item
ADD_ZERO_QUANTITY_TO_CART = 3
# can remove quantity greater than in the cart
REMOVE_QUANTITY_EXCEEDS_CART = 4
# if customer removes units of an item, the entire item is removed from cart
ALWAYS_REMOVE_ENTIRE_ITEM_FROM_CART = 5
# if customer removes all units of an item, the product_id is still in cart
NEVER_REMOVE_PRODUCT_ID_FROM_CART = 6
# checkout modifies inventory before checking all items have sufficient stock
CHECKOUT_CORRUPTS_INVENTORY = 7
# checkout never updates the store's inventory
CHECKOUT_DOES_NOT_UPDATE_INVENTORY = 8
# doesn't empty cart after checkout
CHECKOUT_NEVER_EMPTIES_CART = 9
# checkout always empties the cart, even if checkout fails
CHECKOUT_ALWAYS_EMPTIES_CART = 10


def config(envvar, default="", cast=None):
    """Like decouple.config, read a variable from the environment, 
    with optional casting.  This is so we don't require the decouple package.
    """
    value = os.getenv(envvar)
    if not value and default:
        value = default
    if value and cast:
        return cast(value)
    return value
