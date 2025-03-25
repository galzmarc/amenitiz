// import { FaShoppingCart } from "react-icons/fa"
import { BrowserRouter as Router, Route, Routes } from "react-router"

import CartPage from "./components/CartPage"
import ProductsPage from "./components/ProductsPage"

import "./styles.css"

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/cart" element={<CartPage />} />
      </Routes>
    </Router>
  )
}


{/* <FaShoppingCart 
  className="cart-icon" 
  onClick={() => setCartVisible(!cartVisible)} 
/> */}

