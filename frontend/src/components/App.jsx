import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Product } from "./product";
import CreateProduct from "./CreateProduct";
import CartPage from "./CartPage";
import Navbar from "./Navbar";
function App() {
  const [products, setProducts] = useState(null);
  const [cartProducts, setCartProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    img_url: "",
  });
  function handleChange(event) {
    const { name, value } = event.target;
    setNewProduct((prevproduct) => {
      return {
        ...prevproduct,
        [name]: value,
      };
    });
  }

  function handleAdd(event) {
    event.preventDefault();
    fetch("http://127.0.0.1:5000/api/add-product", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newProduct),
    })
      .then(() => {
        return fetch("http://127.0.0.1:5000/api/products");
      })
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setNewProduct({ name: "", price: "", image_url: "" });
      })
      .catch((err) => console.error("Error:", err));
  }

  async function handleAddToCart(event, productID) {
    event.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/api/add/cart", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_id: productID }),
      });

      const data = await response.json();
      console.log("Success:", data);
    } catch (err) {
      console.error("Error:", err);
    }
  }

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/products")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching:", err));
  }, []);
  console.log();
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/cart-products")
      .then((res) => res.json())
      .then((data) => {
        if (!data.error) {
          setCartProducts(data);
        } else {
          setCartProducts([]);
        }
      })
      .catch((err) => console.error("Error fetching:", err));
  }, []);
  console.log("Current cartProducts state:", cartProducts);
  const cartTotal = cartProducts.reduce(
    (sum, item) => sum + item.price * (item.quantity || 1),
    0
  );
  if (!products) {
    return <p>Loading product...</p>;
  }

  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route
          path="/"
          element={
            <div>
              <CreateProduct
                onChange={handleChange}
                onSubmit={handleAdd}
                newProduct={newProduct}
              />
              {products.map((product, index) => (
                <Product
                  key={index}
                  name={product.name}
                  price={product.price}
                  img={product.image_url}
                  onAddToCart={(event) => handleAddToCart(event, product.id)}
                />
              ))}
            </div>
          }
        />
        <Route
          path="/CartPage"
          element={<CartPage cartProducts={cartProducts} total={cartTotal} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
