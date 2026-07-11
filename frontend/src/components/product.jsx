import React from "react";
import "../styles.css";

function Product(props) {
  return (
    <div className="Product">
      <h1>{props.name}</h1>
      <p>image of product</p>
      <p>price: ${props.price}</p>
      <button>add to cart</button>
      <button>buy now</button>
    </div>
  );
}

export default Product;
