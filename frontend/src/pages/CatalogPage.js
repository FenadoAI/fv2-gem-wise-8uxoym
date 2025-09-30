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
