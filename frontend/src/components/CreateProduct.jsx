import { useState } from "react";

function CreateProduct() {
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    img_url: "",
  });
  return (
    <form>
      <h2>new product</h2>
      <input type="text" name="productName" placeholder="product name" />
      <input type="number" placeholder="price" />
      <input type="file" placeholder="choose file for product image" />
    </form>
  );
}

export default CreateProduct;
