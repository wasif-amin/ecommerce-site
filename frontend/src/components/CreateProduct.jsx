import { useState } from "react";

function CreateProduct(props) {
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    img_url: "",
  });
  return (
    <form onSubmit={props.onSubmit}>
      <h2>new product</h2>
      <input
        type="text"
        name="name"
        placeholder="product name"
        value={props.newProduct.name}
        onChange={props.onChange}
      />
      <input
        type="number"
        placeholder="price"
        name="price"
        value={props.newProduct.price}
        onChange={props.onChange}
      />
      <input
        type="text"
        placeholder="choose file for product image"
        name="image_url"
        value={props.newProduct.image_url}
        onChange={props.onChange}
      />
      <button type="submit">Add Product</button>
    </form>
  );
}

export default CreateProduct;
