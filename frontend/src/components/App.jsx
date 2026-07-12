import React, { useState, useEffect } from "react";
import Product from "./product";

function App() {
  const [products, setProducts] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/products")
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching:", err));
  }, []);
  console.log();

  if (!products) {
    return <p>Loading product...</p>;
  }

  return (
    <div>
      {products.map((product, index) => (
        <Product
          key={index}
          name={product.name}
          price={product.price}
          img={product.image_url}
        />
      ))}
    </div>
  );
}

export default App;
