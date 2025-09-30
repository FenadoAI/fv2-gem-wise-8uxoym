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
