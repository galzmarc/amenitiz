# Cash Register API

This is a cash register (shopping cart) API built with FastAPI and SQLModel, implementing a checkout system with product discounts.

### Requirements
Add products to a cart and compute the total price. Items may be added in any order.

## Discount Rules

| Product  | Code | Unit Price | Discount Rule | 
| ------------- | ------------- | ------------- | ------------- |
| Green Tea  | `gr1`  | €3.11 | Buy 1 Get 1 Free |
| Strawberries  | `sr1`  | €5.00 | Buy 3+, price drops to €4.50 |
| Coffee | `cf1`  | €11.23 | Buy 3+, price drops to 2/3 of the original price |

## API Endpoints

### Products

| Method  | Endpoint | Description | 
| ------------- | ------------- | ------------- |
| `GET`  | `/products/`  | Get all products  |
| `GET`  | `/products/{code}`  | Get a single product by code |

### Shopping Cart

| Method  | Endpoint | Description | 
| ------------- | ------------- | ------------- |
| `GET`  | `/cart/`  | Get items and total price (with discounts)  |
| `POST`  | `/cart/`  | Add a product to the cart |
| `PUT`  | `/cart/{code}` | Update quantity of a product in cart |
| `DELETE`  | `/cart/{code}` | Remove a product from cart |

## Sample requests

**Get all products**
```
GET /products/
```
Response:
```
[
  {"code": "gr1", "name": "Green Tea", "price": 3.11},
  {"code": "sr1", "name": "Strawberries", "price": 5.00},
  {"code": "cf1", "name": "Coffee", "price": 11.23},
]
```

**Add product to cart**
```
POST /cart/
Content-Type: application/json
```
Body:
```
{
  "code": "sr1",
  "quantity": 3
}
```
Response:
```
{"message": "Added 3 x sr1 to cart"}
```

**Get cart total**
```
GET /cart/
```
Response:
```
{
  "items": {
    "sr1": 3,
    "gr1": 1
  },
  "total": 16.61
}
```