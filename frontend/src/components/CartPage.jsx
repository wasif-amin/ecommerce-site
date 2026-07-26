import { CartProduct } from "./product";
export default function CartPage({ cartProducts, total, onRemove }) {
  return (
    <div>
      <h2>Your Shopping Cart</h2>
      {cartProducts.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div>
          {cartProducts.map((item, index) => (
            <CartProduct key={`${item.id}-${index}`} item={item} onRemove={onRemove} />
          ))}
          <h3>total: {total.toFixed(2)}</h3>
        </div>
      )}
    </div>
  );
}
