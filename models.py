from sqlmodel import Field, SQLModel, Session, SQLModel, select
from pydantic import BaseModel
from abc import ABC, abstractmethod

# --- Using the Strategy Design Pattern ---

class Product(SQLModel, table=True):
    __table_args__ = {'keep_existing': True} # Had to add this line to write the tests
    code: str = Field(default=None, primary_key=True)
    name: str
    price: float = Field(ge=0) # Added field validation, non negative

    def apply_discount(self, quantity):
        return self.price * quantity

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, product: Product, quantity: int) -> float:
        pass

class GreenTeaDiscount(DiscountStrategy):    
    # Buy 1 Get 1 Free
    def apply_discount(self, product: Product, quantity: int) -> float:
        return product.price * (quantity // 2 + quantity % 2)
    
class StrawberriesDiscount(DiscountStrategy):
    # If you buy 3 or more strawberries, the price should drop to 4.50€
    def apply_discount(self, product: Product, quantity: int) -> float:
        unit_price = 4.50 if quantity >= 3 else product.price
        return unit_price * quantity

class CoffeeDiscount(DiscountStrategy):
    # If you buy 3 or more, price is 2/3 of original price
    def apply_discount(self, product: Product, quantity: int) -> float:
        unit_price = (2 / 3) * product.price if quantity >= 3 else product.price
        return unit_price * quantity

class NoDiscount(DiscountStrategy):
    def apply_discount(self, product: Product, quantity: int) -> float:
        return product.price * quantity

class Cart:
    def __init__(self, strategy_map=None):
        self.items = {} # { { product_code: { product_name, quantity } }
        self.strategy_map = strategy_map or {
            "gr1": GreenTeaDiscount(),
            "sr1": StrawberriesDiscount(),
            "cf1": CoffeeDiscount()
        }

    def add(self, product_code, product_name, quantity):
        # Add a product or update quantity
        if product_code in self.items:
            self.items[product_code]["quantity"] += quantity
        else:
            self.items[product_code] = {"name": product_name, "quantity": quantity}

    def remove(self, product_code):
        if product_code in self.items:
            self.items.pop(product_code)

    def update(self, product_code, quantity):
        if product_code in self.items:
            self.items[product_code]["quantity"] = quantity

    def total(self, session: Session):
        # Get total price (with discounts) of items in the cart
        total_price = 0.0

        for product_code, details in self.items.items():
            quantity = details["quantity"]

            product = session.exec(select(Product).where(Product.code == product_code)).first()
            
            if product:
                # Apply discount based on product type
                strategy = self.strategy_map.get(product_code, NoDiscount())
                total_price += strategy.apply_discount(product, quantity)

        return total_price

class CartItem(BaseModel):
    code: str
    quantity: int = Field(ge=0) # Added field validation, non negative