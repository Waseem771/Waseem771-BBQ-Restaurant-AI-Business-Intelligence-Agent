// src/components/Configuration.jsx
import React, { useState } from 'react';
import { addProduct } from '../services/productService';

export default function Configuration() {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [price, setPrice] = useState('');
  const [status, setStatus] = useState(null); // success or error message

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    const product = {
      name: name.trim(),
      category: category.trim(),
      unit_price: parseFloat(price),
    };
    try {
      const res = await addProduct(product);
      if (res && res.success) {
        setStatus({ type: 'success', msg: `Product added (ID: ${res.product_id})` });
        setName('');
        setCategory('');
        setPrice('');
      } else {
        setStatus({ type: 'error', msg: 'Failed to add product' });
      }
    } catch (err) {
      setStatus({ type: 'error', msg: err.message || 'Error adding product' });
    }
  };

  return (
    <section className="config-section" style={{ padding: '2rem' }}>
      <h2>⚙️ Add Product Manually</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: '400px', marginTop: '1rem' }}>
        <div style={{ marginBottom: '0.75rem' }}>
          <label htmlFor="product-name" style={{ display: 'block', marginBottom: '0.25rem' }}>Product Name</label>
          <input
            id="product-name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{ width: '100%', padding: '0.4rem' }}
          />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label htmlFor="product-category" style={{ display: 'block', marginBottom: '0.25rem' }}>Category</label>
          <input
            id="product-category"
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
            style={{ width: '100%', padding: '0.4rem' }}
          />
        </div>
        <div style={{ marginBottom: '0.75rem' }}>
          <label htmlFor="product-price" style={{ display: 'block', marginBottom: '0.25rem' }}>Price (PKR)</label>
          <input
            id="product-price"
            type="number"
            min="0"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
            style={{ width: '100%', padding: '0.4rem' }}
          />
        </div>
        <button type="submit" style={{ padding: '0.5rem 1rem', background: '#D84C1A', color: '#fff', border: 'none', borderRadius: 4 }}>
          Add Product
        </button>
      </form>
      {status && (
        <p style={{ marginTop: '1rem', color: status.type === 'success' ? '#27AE60' : '#E74C3C' }}>
          {status.msg}
        </p>
      )}
    </section>
  );
}
