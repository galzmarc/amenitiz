from sqlmodel import Field, SQLModel, Session, SQLModel, select
from pydantic import BaseModel


class Product(SQLModel, table=True):
    __table_args__ = {'keep_existing': True} # Had to add this line to write the tests
    code: str = Field(default=None, primary_key=True)
    name: str
    price: float = Field(ge=0) # Added field validation, non negative

    def apply_discount(self, quantity):
        return self.price * quantity
    
class GreenTea():
    def __init__(self, product: Product):
        self.product = product
    
    # Buy 1 Get 1 Free
    def apply_discount(self, quantity):
        return self.product.price * (quantity // 2 + quantity % 2)
    
class Strawberries():
    def __init__(self, product: Product):
        self.product = product

    # If you buy 3 or more strawberries, the price should drop to 4.50€
    def apply_discount(self, quantity):
        unit_price = 4.50 if quantity >= 3 else self.product.price
        return unit_price * quantity

class Coffee():
    def __init__(self, product: Product):
        self.product = product

    # If you buy 3 or more, price is 2/3 of original price
    def apply_discount(self, quantity):
        unit_price = (2 / 3) * self.product.price if quantity >= 3 else self.product.price
        return unit_price * quantity

class Cart:
    def __init__(self):
        self.items = {} # { { product_code: { product_name, quantity } }

    def add(self, product_code, product_name, quantity):
        # Add a product or update quantity
        if product_code in self.items:
            self.items[product_code]["quantity"] += quantity
        else:
            self.items[product_code] = {"name": product_name, "quantity": quantity}

    def remove(self, product_code):
        # Remove product from cart
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
                if product_code == "gr1":
                    discounted_product = GreenTea(product)
                elif product_code == "sr1":
                    discounted_product = Strawberries(product)
                elif product_code == "cf1":
                    discounted_product = Coffee(product)
                else:
                    discounted_product = product
                
                total_price += discounted_product.apply_discount(quantity)

        return total_price

class CartItem(BaseModel):
    code: str
    quantity: int = Field(ge=0) # Added field validation, non negative