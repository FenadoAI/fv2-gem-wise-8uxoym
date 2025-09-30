#!/bin/bash

# Script to create all frontend pages for the jewellery store

# Create CatalogPage
cat > /workspace/repo/frontend/src/pages/CatalogPage.js << 'CATALOG_EOF'
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { catalogApi } from '../api/client';

export default function CatalogPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    metal_type: '',
    search: '',
    min_price: '',
    max_price: ''
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchItems();
  }, [page, filters]);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const params = { page, limit: 12, ...filters };
      const response = await catalogApi.getItems(params);
      setItems(response.data.items);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error('Failed to fetch items:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPage(1);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link to="/" className="text-2xl font-serif font-bold text-amber-800">
              JewelCraft Pro
            </Link>
            <nav className="flex gap-6">
              <Link to="/" className="text-gray-700 hover:text-amber-700">Home</Link>
              <Link to="/catalog" className="text-amber-700 font-semibold">Catalog</Link>
              <Link to="/login" className="text-gray-700 hover:text-amber-700">Admin</Link>
            </nav>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-serif font-bold text-amber-900 mb-8">Jewellery Collection</h1>

        {/* Filters */}
        <div className="bg-white p-6 rounded-lg shadow-md mb-8">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <input
              type="text"
              placeholder="Search..."
              className="border rounded px-3 py-2"
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
            />
            <select
              className="border rounded px-3 py-2"
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
            >
              <option value="">All Categories</option>
              <option value="ring">Ring</option>
              <option value="necklace">Necklace</option>
              <option value="bracelet">Bracelet</option>
              <option value="earring">Earring</option>
              <option value="pendant">Pendant</option>
            </select>
            <select
              className="border rounded px-3 py-2"
              value={filters.metal_type}
              onChange={(e) => handleFilterChange('metal_type', e.target.value)}
            >
              <option value="">All Metals</option>
              <option value="gold">Gold</option>
              <option value="silver">Silver</option>
              <option value="platinum">Platinum</option>
              <option value="white_gold">White Gold</option>
              <option value="rose_gold">Rose Gold</option>
            </select>
            <input
              type="number"
              placeholder="Min Price ($)"
              className="border rounded px-3 py-2"
              value={filters.min_price}
              onChange={(e) => handleFilterChange('min_price', e.target.value ? parseInt(e.target.value) * 100 : '')}
            />
            <input
              type="number"
              placeholder="Max Price ($)"
              className="border rounded px-3 py-2"
              value={filters.max_price}
              onChange={(e) => handleFilterChange('max_price', e.target.value ? parseInt(e.target.value) * 100 : '')}
            />
          </div>
        </div>

        {/* Items Grid */}
        {loading ? (
          <div className="text-center py-12">Loading...</div>
        ) : items.length === 0 ? (
          <div className="text-center py-12 text-gray-500">No items found</div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {items.map((item) => (
                <Link
                  key={item.id}
                  to={`/catalog/${item.id}`}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition"
                >
                  <img
                    src={item.images[0] || 'https://via.placeholder.com/300?text=Jewellery'}
                    alt={item.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-800 mb-1 line-clamp-1">{item.name}</h3>
                    <p className="text-sm text-gray-600 mb-2 capitalize">{item.metal_type}</p>
                    <div className="text-lg font-bold text-amber-700">
                      ${(item.price / 100).toFixed(2)}
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center gap-2 mt-8">
                <button
                  onClick={() => setPage(p => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 border rounded disabled:opacity-50"
                >
                  Previous
                </button>
                <span className="px-4 py-2">
                  Page {page} of {totalPages}
                </span>
                <button
                  onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 border rounded disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
CATALOG_EOF

echo "Created CatalogPage.js"

# Create ProductDetailPage
cat > /workspace/repo/frontend/src/pages/ProductDetailPage.js << 'PRODUCT_EOF'
import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { catalogApi, ordersApi } from '../api/client';

export default function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showOrderForm, setShowOrderForm] = useState(false);
  const [orderData, setOrderData] = useState({
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    quantity: 1,
    shipping_address: {
      line1: '',
      line2: '',
      city: '',
      state: '',
      zip: '',
      country: 'USA'
    },
    notes: ''
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchItem();
  }, [id]);

  const fetchItem = async () => {
    try {
      const response = await catalogApi.getItem(id);
      setItem(response.data);
    } catch (error) {
      console.error('Failed to fetch item:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitOrder = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await ordersApi.create({
        ...orderData,
        items: [{ item_id: id, quantity: orderData.quantity }]
      });
      setSuccess(true);
    } catch (error) {
      setError(error.response?.data?.detail?.error?.message || 'Failed to place order');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  if (!item) {
    return <div className="flex items-center justify-center h-screen">Item not found</div>;
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg text-center max-w-md">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="text-2xl font-bold mb-4">Order Placed!</h2>
          <p className="text-gray-600 mb-6">
            Your order has been placed successfully. You will receive a confirmation email shortly.
          </p>
          <Link to="/catalog" className="bg-amber-600 text-white px-6 py-2 rounded-lg inline-block">
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link to="/" className="text-2xl font-serif font-bold text-amber-800">
              JewelCraft Pro
            </Link>
            <nav className="flex gap-6">
              <Link to="/" className="text-gray-700 hover:text-amber-700">Home</Link>
              <Link to="/catalog" className="text-gray-700 hover:text-amber-700">Catalog</Link>
            </nav>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <Link to="/catalog" className="text-amber-700 mb-4 inline-block">&larr; Back to Catalog</Link>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <img
              src={item.images[0] || 'https://via.placeholder.com/600?text=Jewellery'}
              alt={item.name}
              className="w-full rounded-lg shadow-lg"
            />
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md">
            <h1 className="text-3xl font-bold text-gray-800 mb-4">{item.name}</h1>
            <div className="text-4xl font-bold text-amber-700 mb-6">
              ${(item.price / 100).toFixed(2)}
            </div>

            <div className="space-y-3 mb-6">
              <p><span className="font-semibold">Code:</span> {item.item_code}</p>
              <p><span className="font-semibold">Category:</span> {item.category}</p>
              <p><span className="font-semibold">Metal:</span> {item.metal_type}</p>
              <p><span className="font-semibold">Weight:</span> {item.weight}g</p>
              {item.stones && <p><span className="font-semibold">Stones:</span> {item.stones}</p>}
              <p><span className="font-semibold">Available:</span> {item.quantity} in stock</p>
            </div>

            <p className="text-gray-600 mb-6">{item.description}</p>

            {!showOrderForm ? (
              <button
                onClick={() => setShowOrderForm(true)}
                className="w-full bg-amber-600 hover:bg-amber-700 text-white font-semibold py-3 rounded-lg"
              >
                Order Now (Cash on Delivery)
              </button>
            ) : (
              <form onSubmit={handleSubmitOrder} className="space-y-4">
                <h3 className="font-bold text-lg">Order Details</h3>
                {error && <div className="bg-red-100 text-red-700 p-3 rounded">{error}</div>}

                <input
                  type="text"
                  placeholder="Full Name"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={orderData.customer_name}
                  onChange={(e) => setOrderData({...orderData, customer_name: e.target.value})}
                />
                <input
                  type="email"
                  placeholder="Email"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={orderData.customer_email}
                  onChange={(e) => setOrderData({...orderData, customer_email: e.target.value})}
                />
                <input
                  type="tel"
                  placeholder="Phone"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={orderData.customer_phone}
                  onChange={(e) => setOrderData({...orderData, customer_phone: e.target.value})}
                />
                <input
                  type="number"
                  min="1"
                  max={item.quantity}
                  placeholder="Quantity"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={orderData.quantity}
                  onChange={(e) => setOrderData({...orderData, quantity: parseInt(e.target.value)})}
                />

                <h4 className="font-semibold mt-4">Shipping Address</h4>
                <input
                  type="text"
                  placeholder="Address Line 1"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={orderData.shipping_address.line1}
                  onChange={(e) => setOrderData({...orderData, shipping_address: {...orderData.shipping_address, line1: e.target.value}})}
                />
                <input
                  type="text"
                  placeholder="Address Line 2"
                  className="w-full border rounded px-3 py-2"
                  value={orderData.shipping_address.line2}
                  onChange={(e) => setOrderData({...orderData, shipping_address: {...orderData.shipping_address, line2: e.target.value}})}
                />
                <div className="grid grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="City"
                    required
                    className="border rounded px-3 py-2"
                    value={orderData.shipping_address.city}
                    onChange={(e) => setOrderData({...orderData, shipping_address: {...orderData.shipping_address, city: e.target.value}})}
                  />
                  <input
                    type="text"
                    placeholder="State"
                    required
                    className="border rounded px-3 py-2"
                    value={orderData.shipping_address.state}
                    onChange={(e) => setOrderData({...orderData, shipping_address: {...orderData.shipping_address, state: e.target.value}})}
                  />
                  <input
                    type="text"
                    placeholder="ZIP"
                    required
                    className="border rounded px-3 py-2"
                    value={orderData.shipping_address.zip}
                    onChange={(e) => setOrderData({...orderData, shipping_address: {...orderData.shipping_address, zip: e.target.value}})}
                  />
                  <input
                    type="text"
                    placeholder="Country"
                    required
                    className="border rounded px-3 py-2"
                    value={orderData.shipping_address.country}
                    onChange={(e) => setOrderData({...orderData, shipping_address: {...orderData.shipping_address, country: e.target.value}})}
                  />
                </div>

                <textarea
                  placeholder="Special instructions (optional)"
                  className="w-full border rounded px-3 py-2"
                  rows="3"
                  value={orderData.notes}
                  onChange={(e) => setOrderData({...orderData, notes: e.target.value})}
                />

                <div className="flex gap-4">
                  <button
                    type="button"
                    onClick={() => setShowOrderForm(false)}
                    className="flex-1 border border-gray-300 py-2 rounded-lg"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="flex-1 bg-amber-600 text-white py-2 rounded-lg disabled:opacity-50"
                  >
                    {submitting ? 'Placing Order...' : 'Place Order'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
PRODUCT_EOF

echo "Created ProductDetailPage.js"
# Create LoginPage
cat > /workspace/repo/frontend/src/pages/LoginPage.js << 'LOGIN_EOF'
import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/admin/dashboard" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);

    if (result.success) {
      navigate('/admin/dashboard');
    } else {
      setError(result.error);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold text-center text-blue-900 mb-8">
          Admin Login
        </h2>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-gray-700 font-semibold mb-2">Email</label>
            <input
              type="email"
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@jewelcraft.com"
            />
          </div>

          <div>
            <label className="block text-gray-700 font-semibold mb-2">Password</label>
            <input
              type="password"
              required
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <a href="/" className="text-blue-600 hover:text-blue-800">
            &larr; Back to Home
          </a>
        </div>
      </div>
    </div>
  );
}
LOGIN_EOF

echo "Created LoginPage.js"

# Create DashboardPage
cat > /workspace/repo/frontend/src/pages/DashboardPage.js << 'DASHBOARD_EOF'
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { inventoryApi, ordersApi } from '../api/client';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState({
    totalItems: 0,
    totalOrders: 0,
    pendingOrders: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [inventoryRes, ordersRes, pendingRes] = await Promise.all([
        inventoryApi.getAll({ limit: 1 }),
        ordersApi.getAll({ limit: 1 }),
        ordersApi.getAll({ limit: 1, status: 'pending' })
      ]);

      setStats({
        totalItems: inventoryRes.data.total,
        totalOrders: ordersRes.data.total,
        pendingOrders: pendingRes.data.total
      });
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-900">Admin Dashboard</h1>
            <div className="flex items-center gap-4">
              <span className="text-gray-600">
                {user?.username} ({user?.role})
              </span>
              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-500 text-sm font-semibold mb-2">Total Items</h3>
            <p className="text-3xl font-bold text-blue-900">{stats.totalItems}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-500 text-sm font-semibold mb-2">Total Orders</h3>
            <p className="text-3xl font-bold text-blue-900">{stats.totalOrders}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-500 text-sm font-semibold mb-2">Pending Orders</h3>
            <p className="text-3xl font-bold text-orange-600">{stats.pendingOrders}</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Link
              to="/admin/inventory"
              className="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg text-center font-semibold"
            >
              Manage Inventory
            </Link>
            <Link
              to="/admin/orders"
              className="bg-green-500 hover:bg-green-600 text-white p-4 rounded-lg text-center font-semibold"
            >
              View Orders
            </Link>
            {user?.role === 'owner' && (
              <Link
                to="/admin/users"
                className="bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-lg text-center font-semibold"
              >
                Manage Users
              </Link>
            )}
            <a
              href="/"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-500 hover:bg-gray-600 text-white p-4 rounded-lg text-center font-semibold"
            >
              View Public Site
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
DASHBOARD_EOF

echo "Created DashboardPage.js"

echo "All pages created successfully!"
