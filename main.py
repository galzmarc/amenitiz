from fastapi import FastAPI
from models import products, Cart

app = FastAPI()
cart = Cart()

# API for products
@app.get("/products/")
async def get_all():
    return [
        {"code": p.product_code, "name": p.name, "price": p.price}
        for p in products.values()
    ]

@app.get("/products/{code}")
async def get_one(code):
    product = products.get(code)
    if not product:
        return {"error": "Product not found"}
    return {"code": product.product_code, "name": product.name, "price": product.price}

# API for shopping cart
@app.get("/cart/")
async def get_cart_total():
    return {"total": cart.total(products)}

@app.post("/cart/")
async def add_to_cart(product_code, quantity):
    if product_code not in products:
        return {"error": "Product not found"}
    cart.add(product_code, quantity)
    return {"message": f"Added {quantity} x {product_code} to cart"}