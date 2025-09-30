import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { catalogApi } from '../api/client';

export default function HomePage() {
  const [featuredItems, setFeaturedItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedItems();
  }, []);

  const fetchFeaturedItems = async () => {
    try {
      const response = await catalogApi.getItems({ limit: 6 });
      setFeaturedItems(response.data.items);
    } catch (error) {
      console.error('Failed to fetch featured items:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <Link to="/" className="text-2xl font-serif font-bold text-amber-800">
              JewelCraft Pro
            </Link>
            <nav className="flex gap-6">
              <Link to="/catalog" className="text-gray-700 hover:text-amber-700">
                Catalog
              </Link>
              <Link to="/login" className="text-gray-700 hover:text-amber-700">
                Admin
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 text-center">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-5xl font-serif font-bold text-amber-900 mb-6">
            Elegant Jewellery,<br />Simplified Management
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Discover exquisite handcrafted jewellery with secure Cash on Delivery
          </p>
          <Link
            to="/catalog"
            className="inline-block bg-amber-600 hover:bg-amber-700 text-white font-semibold px-8 py-3 rounded-lg transition"
          >
            Browse Collection
          </Link>
        </div>
      </section>

      {/* Featured Items */}
      <section className="py-16 max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-serif font-bold text-center text-amber-900 mb-12">
          Featured Collection
        </h2>

        {loading ? (
          <div className="text-center">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredItems.map((item) => (
              <Link
                key={item.id}
                to={`/catalog/${item.id}`}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition"
              >
                <img
                  src={item.images[0] || 'https://via.placeholder.com/400x300?text=Jewellery'}
                  alt={item.name}
                  className="w-full h-64 object-cover"
                />
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">{item.name}</h3>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">{item.description}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-2xl font-bold text-amber-700">
                      ${(item.price / 100).toFixed(2)}
                    </span>
                    <span className="text-sm text-gray-500 capitalize">{item.metal_type}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* Features */}
      <section className="py-16 bg-amber-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl mb-4">💎</div>
              <h3 className="text-xl font-semibold mb-2">Authentic Quality</h3>
              <p className="text-gray-600">100% genuine precious metals and stones</p>
            </div>
            <div>
              <div className="text-4xl mb-4">🚚</div>
              <h3 className="text-xl font-semibold mb-2">Cash on Delivery</h3>
              <p className="text-gray-600">Pay securely when you receive your order</p>
            </div>
            <div>
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-xl font-semibold mb-2">Handcrafted</h3>
              <p className="text-gray-600">Each piece crafted with precision and care</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>&copy; 2025 JewelCraft Pro. All rights reserved.</p>
          <Link to="/login" className="text-amber-400 hover:text-amber-300 mt-2 inline-block">
            Admin Login
          </Link>
        </div>
      </footer>
    </div>
  );
}