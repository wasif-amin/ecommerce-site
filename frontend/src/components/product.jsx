import React from "react";
import "../styles.css";

function Product({ name, price, img, onAddToCart }) {
  return (
    <div className="Product">
      <h1>{name}</h1>
      <img src={img} alt={name} style={{ width: "200px", height: "200px" }} />

      <p>price: ${price}</p>
      <div className="button-container">
        <button onClick={onAddToCart}>add to cart</button>
        <button>buy now</button>
      </div>
    </div>
  );
}

export default Product;
