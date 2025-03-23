import pytest
from sqlmodel import SQLModel, Session, create_engine, select
from sqlmodel.pool import StaticPool

import sys
sys.path.append('../amenitiz')

from models import Product, GreenTea, Strawberries, Coffee, Cart

# ----- Tests for classes -----

def test_product():
    product = Product(code="gr1", name="Green Tea", price=3.11)
    assert product.apply_discount(2) == 6.22

def test_green_tea_discount():
    product = Product(code="gr1", name="Green Tea", price=3.11)
    green_tea = GreenTea(product)
    assert green_tea.apply_discount(2) == 3.11
    assert green_tea.apply_discount(3) == 6.22

def test_strawberries_discount():
    product = Product(code="sr1", name="Strawberries", price=5.00)
    strawberries = Strawberries(product)
    assert strawberries.apply_discount(2) == 10.00
    assert strawberries.apply_discount(3) == 13.50

def test_coffee_discount():
    product = Product(code="cf1", name="Coffee", price=11.23)
    coffee = Coffee(product)
    assert coffee.apply_discount(2) == 22.46
    assert coffee.apply_discount(3) == 22.46

def test_cart_add_remove():
    cart = Cart()
    cart.add("gr1", 2)
    assert cart.items["gr1"] == 2

    cart.remove("gr1")
    assert "gr1" not in cart.items


# ----- Tests for APIs -----


# Creating test DB
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        products = [
            Product(code="gr1", name="Green Tea", price=3.11),
            Product(code="sr1", name="Strawberries", price=5.00),
            Product(code="cf1", name="Coffee", price=11.23),
        ]
        session.add_all(products)
        session.commit()

        yield session

@pytest.mark.parametrize("items, expected_total", [
    (["gr1", "gr1"], 3.11),
    (["sr1", "sr1", "gr1", "sr1"], 16.61),
    (["gr1", "cf1", "sr1", "cf1", "cf1"], 30.57),
])

def test_cart_total(items, expected_total, session: Session):
    cart = Cart()
    for item in items:
        cart.add(item, 1) 

    assert cart.total(session) == expected_total
