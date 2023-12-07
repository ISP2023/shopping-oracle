"""Configuration for instrumented target code."""
import os

# cart only checks if incremental quantity added <= stock
BYPASS_STOCK_LIMIT = 1
# add product id of non-existing product to cart
ADD_NONEXISTENT_PRODUCT = 2
# can remove quantity greater than in the cart
REMOVE_QUANTITY_EXCEEDS_CART = 3
# checkout modifies inventory before checking all
CHECKOUT_CORRUPTS_INVENTORY = 4
# checkout never updates the store's inventory
CHECKOUT_DOES_NOT_UPDATE_INVENTORY = 5
# doesn't empty cart after checkout
CHECKOUT_NOT_EMPTY_CART = 6
# can add zero quantity of an item
ADD_ZERO_QUANTITY_TO_CART = 7


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
