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

      if (response.ok) {
        const data = await response.json();
        console.log("Success:", data);

        const cartResponse = await fetch(
          "http://127.0.0.1:5000/api/cart-products"
        );
        const cartData = await cartResponse.json();
        setCartProducts(cartData);
      }
    } catch (err) {
      console.error("Error:", err);
    }
  }

  async function handleRemoveFromCart(productId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/remove-from-cart/${productId}`,
        {
          method: "DELETE",
        }
      );
      if (response.ok) {
        setCartProducts((prevProducts) =>
          prevProducts.filter((item) => item.id !== productId)
        );
      }
    } catch (err) {
      console.error("Error removing item:", err);
    }
  }

  async function handleRemoveFromStore(productId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/remove-from-store/${productId}`,
        {
          method: "DELETE",
        }
      );
      if (response.ok) {
        setProducts((prevProducts) =>
          prevProducts.filter((p) => p.id !== productId)
        );
      }
    } catch (err) {
      console.error("Error removing item:", err);
    }
  }
  async function handleIncrease(id) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/update-cart-item/${id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ change: 1 }),
        }
      );
      if (response.ok) {
        setCartProducts((prevCart) =>
          prevCart.map((item) =>
            item.id === id ? { ...item, quantity: item.quantity + 1 } : item
          )
        );
      }
    } catch (err) {
      console.error("Error increasing quantity:", err);
    }
  }

  async function handleDecrease(id) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/update-cart-item/${id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ change: -1 }),
        }
      );

      if (response.ok) {
        setCartProducts((prevCart) =>
          prevCart.map((item) =>
            item.id === id ? { ...item, quantity: item.quantity - 1 } : item
          )
        );
      }
    } catch (err) {
      console.error("Error decreasing quantity:", err);
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
                  onRemove={() => handleRemoveFromStore(product.id)}
                />
              ))}
            </div>
          }
        />
        <Route
          path="/CartPage"
          element={
            <CartPage
              cartProducts={cartProducts}
              total={cartTotal}
              onRemove={handleRemoveFromCart}
              onIncrease={handleIncrease}
              onDecrease={handleDecrease}
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
