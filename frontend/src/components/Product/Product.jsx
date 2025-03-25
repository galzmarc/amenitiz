import styles from "./product.module.css"

export default function Product({product}) {
  
  const addToCart = (code, quantity) => {
    fetch("http://localhost:8000/cart/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, quantity: Number(quantity) })
    })
    .then(() => alert("Added to cart"))
  }

  return (
    <div className={styles.productTile}>
      <p>{product.name} - €{product.price.toFixed(2)}</p>
      <input className={styles["input-number"]} type="number" min="1" defaultValue="1" id={`qty-${product.code}`} />
      <button className={styles.cartBtn}
        onClick={() => addToCart(product.code, document.getElementById(`qty-${product.code}`).value)}
      >
        Add to Cart
      </button>
    </div>
  )
}