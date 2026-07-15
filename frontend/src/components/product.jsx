import React from "react";
import "../styles.css";

function Product(props) {
  return (
    <div className="Product">
      <h1>{props.name}</h1>
      <img
        src={props.img}
        alt={props.name}
        style={{ width: "200px", height: "200px" }}
      />

      <p>price: ${props.price}</p>
      <button>add to cart</button>
      <button>buy now</button>
    </div>
  );
}

export default Product;
