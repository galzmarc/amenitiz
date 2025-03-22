import pytest
import sys
sys.path.append('../amenitiz')

from models import Cart, products

@pytest.mark.parametrize("items, expected_total", [
    (["gr1", "gr1"], 3.11),
    (["sr1", "sr1", "gr1", "sr1"], 16.61),
    (["gr1", "cf1", "sr1", "cf1", "cf1"], 30.57),
])

def test_cart_total(items, expected_total):
    cart = Cart()
    for item in items:
        cart.add(item, 1)

    assert cart.total(products) == expected_total
