// src/services/productService.js
const BASE = 'http://localhost:8000/api/v1';
export async function addProduct(product) {
  const res = await fetch(`${BASE}/products/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(product),
  });
  if (!res.ok) throw new Error('Failed to add product');
  return await res.json();
}

export async function getAllProducts() {
  const res = await fetch(`${BASE}/products/all`);
  if (!res.ok) throw new Error('Failed to fetch products');
  return await res.json();
}
