class Product:
    def __init__(self, product_code, name, price):
        self.product_code = product_code
        self.name = name
        self.price = price

    def apply_discount(self, quantity):
        return self.price * quantity

class GreenTea(Product):
    # The CEO is a big fan of buy-one-get-one-free offers and green tea
    def apply_discount(self, quantity):
        if quantity % 2 == 0:
            return self.price * quantity / 2
        else:
            return self.price * quantity
        
class Strawberries(Product):
    # If you buy 3 or more strawberries, the price should drop to 4.50€
    def apply_discount(self, quantity):
        unit_price = 4.50 if quantity >= 3 else self.price
        return unit_price * quantity

class Coffee(Product):
    # If 3 or more, price is 2/3 of original price
    def apply_discount(self, quantity):
        unit_price = (2 / 3) * self.price if quantity >= 3 else self.price
        return unit_price * quantity


# Using a dictionary to store products, mimics database
products = {
    "gr1": GreenTea("GR1", "Green Tea", 3.11),
    "sr1": Strawberries("SR1", "Strawberries", 5.00),
    "cf1": Coffee("CF1", "Coffee", 11.23),
}


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, product_code, quantity):
        if product_code in self.items:
            self.items[product_code] += quantity
        else:
            self.items[product_code] = quantity
    
    def total(self, products):
        total_price = 0.0
        for product_code, quantity in self.items.items():
            p = products.get(product_code)
            if p:
                total_price += p.apply_discount(quantity)
        return total_price