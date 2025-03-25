import { useState, useEffect } from 'react'
import { Link } from "react-router"
import Product from './Product/Product'

export default function ProductsPage() {

  const container = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
    gap: "1.5rem",
    padding: "2rem",
  }

  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/products/")
      .then((res) => res.json())
      .then((data) => setProducts(data))
    }, [])

  return (
    <>
      <h1>Products</h1>
      <div style={container}>
        {products.map(product => (
          <Product product={product} key={product.code}/>
        ))}
      </div>
      <Link to="/cart">Go to Cart</Link>
    </>
  )
}
