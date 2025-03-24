from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from .models import Product, Cart, CartItem

def get_session():
    with Session(engine) as session:
        yield session

def create_products():
    products = [
        {"code": "gr1", "name": "Green Tea", "price": 3.11},
        {"code": "sr1", "name": "Strawberries", "price": 5.00},
        {"code": "cf1", "name": "Coffee", "price": 11.23},
    ]
    with Session(engine) as session:
        for prod in products:
            existing_product = session.exec(select(Product).where(Product.code == prod["code"])).first()
            if not existing_product:
                new_product = Product(**prod)
                session.add(new_product)
        
        session.commit()

app = FastAPI()
cart = Cart()

# Initialize DB
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Insert products
create_products()

# ----- API for products -----

@app.get("/products/")
async def get_all(session: Session = Depends(get_session)):
    statement = select(Product)
    results = session.exec(statement)
    return [
        {"code": res.code, "name": res.name, "price": res.price}
        for res in results
    ]

@app.get("/products/{code}")
# This endpoint is actually never used, but it might come in handy if we expand the app.
# Took me 2 secs to write, so there is no point in deleting
async def get_one(*, session: Session = Depends(get_session), code: str):
    statement = select(Product).where(Product.code == code)
    product = session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"code": product.code, "name": product.name, "price": product.price}

# ----- API for shopping cart -----

@app.get("/cart/")
async def get_cart_total(session: Session = Depends(get_session)):
    return {"items": cart.items, "total": cart.total(session)}
    
@app.post("/cart/")
async def add_to_cart(*, session: Session = Depends(get_session), item: CartItem):
    statement = select(Product).where(Product.code == item.code)
    product = session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart.add(item.code, item.quantity)
    return {"message": f"Added {item.quantity} x {item.code} to cart"}

@app.put("/cart/{code}")
async def update_item(*, session: Session = Depends(get_session), code: str, item: CartItem):
    statement = select(Product).where(Product.code == code)
    product = session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if code not in cart.items:
        raise HTTPException(status_code=404, detail="Product not in cart")
    cart.update(code, item.quantity)
    return {"message": f"Updated quantity for {code}: {item.quantity}"}

@app.delete("/cart/{code}")
async def delete_from_cart(*, session: Session = Depends(get_session), code: str):
    statement = select(Product).where(Product.code == code)
    product = session.exec(statement).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if code not in cart.items:
        raise HTTPException(status_code=404, detail="Product not in cart")
    cart.remove(code)
    return {"message": f"Removed {code} from cart"}