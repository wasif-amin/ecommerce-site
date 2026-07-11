import React, { useState, useEffect } from "react";
import Product from "./product";

function App() {
  const [product, setProduct] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/products")
      .then((res) => res.json())
      .then((data) => setProduct(data))
      .catch((err) => console.error("Error fetching:", err));
  }, []);
  if (!product) {
    return <p>Loading product...</p>;
  }

  return <Product name={product.name} price={product.price} />;
}

export default App;
