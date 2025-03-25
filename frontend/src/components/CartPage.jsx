import { useState, useEffect } from 'react'
import { Link } from "react-router"
import styles from "./cartpage.module.css"

export default function CartPage() {
  const [cart, setCart] = useState({ items: {}, total: 0 })

  useEffect(() => {
      fetch("http://localhost:8000/cart/")
          .then((res) => res.json())
          .then((data) => setCart(data));
  }, [])

  const updateCart = (code, quantity) => {
      fetch(`http://localhost:8000/cart/${code}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, quantity: Number(quantity) })
      }).then(() => window.location.reload());
  }

  const removeFromCart = (code) => {
      fetch(`http://localhost:8000/cart/${code}`, { method: "DELETE" })
          .then(() => window.location.reload());
  }

  return (
      <div>
          <h1>Shopping Cart</h1>
          {Object.entries(cart.items).length == 0 ? 
            <p>There are no items in the cart</p> :
          <>
          {Object.entries(cart.items).map(([code, {name, quantity}]) => (
            <div className={styles.cartTile} key={code}>
                <p>{name} - Quantity: {quantity}</p>
                <div className={styles.test}>
                    <input className={styles.inputNumber} type="number" min="1" defaultValue={quantity} id={`qty-${code}`} />
                    <button className={styles.cartBtn} onClick={() => updateCart(code, document.getElementById(`qty-${code}`).value)}>Update</button>
                    <button className={styles.cartBtn} onClick={() => removeFromCart(code)}>Remove</button>
                </div>
            </div>
          ))}
          <h2 className={styles.total}>Total: €{cart.total.toFixed(2)}</h2>
          </>
          }  
          <Link to="/">Back to Products</Link>
      </div>
  )
}
