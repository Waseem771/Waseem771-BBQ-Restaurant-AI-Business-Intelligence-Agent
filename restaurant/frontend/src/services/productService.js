// src/services/productService.js
import { apiRequest } from '../lib/api';

export async function addProduct(product) {
  return apiRequest('/products/', {
    method: 'POST',
    body: JSON.stringify(product),
  });
}

export async function getAllProducts() {
  return apiRequest('/products/');
}
