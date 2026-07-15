import React, { useState, useEffect } from "react";
import Product from "./product";
import CreateProduct from "./CreateProduct";

function App() {
  const [products, setProducts] = useState(null);
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
        />
      ))}
    </div>
  );
}

export default App;
