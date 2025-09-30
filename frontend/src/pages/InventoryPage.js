import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { inventoryApi } from '../api/client';

export default function InventoryPage() {
  const { user, logout } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [formData, setFormData] = useState({
    item_code: '',
    name: '',
    description: '',
    category: 'ring',
    price: '',
    weight: '',
    metal_type: 'gold',
    stones: '',
    images: [],
    quantity: '',
    status: 'in_stock'
  });
  const [imageUrl, setImageUrl] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const response = await inventoryApi.getAll({ limit: 100 });
      setItems(response.data.items);
    } catch (error) {
      setError('Failed to fetch inventory');
    } finally {
      setLoading(false);
    }
  };

  const handleAddImage = () => {
    if (imageUrl && formData.images.length < 10) {
      setFormData(prev => ({
        ...prev,
        images: [...prev.images, imageUrl]
      }));
      setImageUrl('');
    }
  };

  const handleRemoveImage = (index) => {
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const submitData = {
        ...formData,
        price: parseInt(formData.price) * 100, // Convert to cents
        weight: parseFloat(formData.weight),
        quantity: parseInt(formData.quantity)
      };

      if (editingItem) {
        await inventoryApi.update(editingItem.id, submitData);
        setSuccess('Item updated successfully');
      } else {
        await inventoryApi.create(submitData);
        setSuccess('Item added successfully');
      }

      setShowForm(false);
      setEditingItem(null);
      resetForm();
      fetchItems();
    } catch (error) {
      setError(error.response?.data?.detail?.error?.message || 'Failed to save item');
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      item_code: item.item_code,
      name: item.name,
      description: item.description,
      category: item.category,
      price: (item.price / 100).toString(),
      weight: item.weight.toString(),
      metal_type: item.metal_type,
      stones: item.stones || '',
      images: item.images,
      quantity: item.quantity.toString(),
      status: item.status
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;

    try {
      await inventoryApi.delete(id);
      setSuccess('Item deleted successfully');
      fetchItems();
    } catch (error) {
      setError('Failed to delete item');
    }
  };

  const resetForm = () => {
    setFormData({
      item_code: '',
      name: '',
      description: '',
      category: 'ring',
      price: '',
      weight: '',
      metal_type: 'gold',
      stones: '',
      images: [],
      quantity: '',
      status: 'in_stock'
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <Link to="/admin/dashboard" className="text-blue-600">&larr; Dashboard</Link>
              <h1 className="text-2xl font-bold">Inventory Management</h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">{user?.username}</span>
              <button onClick={logout} className="text-red-600">Logout</button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
        {success && <div className="bg-green-100 text-green-700 p-3 rounded mb-4">{success}</div>}

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Items ({items.length})</h2>
          <button
            onClick={() => { setShowForm(true); setEditingItem(null); resetForm(); }}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            + Add New Item
          </button>
        </div>

        {showForm && (
          <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
            <h3 className="text-lg font-bold mb-4">{editingItem ? 'Edit Item' : 'Add New Item'}</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Item Code *"
                  required
                  className="border rounded px-3 py-2"
                  value={formData.item_code}
                  onChange={(e) => setFormData({...formData, item_code: e.target.value})}
                />
                <input
                  type="text"
                  placeholder="Name *"
                  required
                  className="border rounded px-3 py-2"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                />
              </div>

              <textarea
                placeholder="Description *"
                required
                className="w-full border rounded px-3 py-2"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />

              <div className="grid grid-cols-3 gap-4">
                <select
                  className="border rounded px-3 py-2"
                  value={formData.category}
                  onChange={(e) => setFormData({...formData, category: e.target.value})}
                >
                  <option value="ring">Ring</option>
                  <option value="necklace">Necklace</option>
                  <option value="bracelet">Bracelet</option>
                  <option value="earring">Earring</option>
                  <option value="pendant">Pendant</option>
                  <option value="bangle">Bangle</option>
                  <option value="chain">Chain</option>
                  <option value="other">Other</option>
                </select>

                <select
                  className="border rounded px-3 py-2"
                  value={formData.metal_type}
                  onChange={(e) => setFormData({...formData, metal_type: e.target.value})}
                >
                  <option value="gold">Gold</option>
                  <option value="silver">Silver</option>
                  <option value="platinum">Platinum</option>
                  <option value="white_gold">White Gold</option>
                  <option value="rose_gold">Rose Gold</option>
                </select>

                <select
                  className="border rounded px-3 py-2"
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                >
                  <option value="in_stock">In Stock</option>
                  <option value="sold">Sold</option>
                  <option value="reserved">Reserved</option>
                  <option value="discontinued">Discontinued</option>
                </select>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <input
                  type="number"
                  placeholder="Price (USD) *"
                  required
                  step="0.01"
                  className="border rounded px-3 py-2"
                  value={formData.price}
                  onChange={(e) => setFormData({...formData, price: e.target.value})}
                />
                <input
                  type="number"
                  placeholder="Weight (grams) *"
                  required
                  step="0.01"
                  className="border rounded px-3 py-2"
                  value={formData.weight}
                  onChange={(e) => setFormData({...formData, weight: e.target.value})}
                />
                <input
                  type="number"
                  placeholder="Quantity *"
                  required
                  className="border rounded px-3 py-2"
                  value={formData.quantity}
                  onChange={(e) => setFormData({...formData, quantity: e.target.value})}
                />
              </div>

              <input
                type="text"
                placeholder="Stones (optional)"
                className="w-full border rounded px-3 py-2"
                value={formData.stones}
                onChange={(e) => setFormData({...formData, stones: e.target.value})}
              />

              <div>
                <label className="block font-semibold mb-2">Images (max 10)</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="url"
                    placeholder="Image URL"
                    className="flex-1 border rounded px-3 py-2"
                    value={imageUrl}
                    onChange={(e) => setImageUrl(e.target.value)}
                  />
                  <button type="button" onClick={handleAddImage} className="bg-gray-500 text-white px-4 py-2 rounded">
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {formData.images.map((url, index) => (
                    <div key={index} className="relative">
                      <img src={url} alt="" className="w-20 h-20 object-cover rounded" />
                      <button
                        type="button"
                        onClick={() => handleRemoveImage(index)}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 text-xs"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
                {formData.images.length === 0 && (
                  <p className="text-red-500 text-sm">At least 1 image is required</p>
                )}
              </div>

              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => { setShowForm(false); setEditingItem(null); resetForm(); }}
                  className="flex-1 border py-2 rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 rounded"
                  disabled={formData.images.length === 0}
                >
                  {editingItem ? 'Update' : 'Add'} Item
                </button>
              </div>
            </form>
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">Loading...</div>
        ) : (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left">Code</th>
                  <th className="px-4 py-3 text-left">Name</th>
                  <th className="px-4 py-3 text-left">Category</th>
                  <th className="px-4 py-3 text-left">Price</th>
                  <th className="px-4 py-3 text-left">Quantity</th>
                  <th className="px-4 py-3 text-left">Status</th>
                  <th className="px-4 py-3 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="border-t">
                    <td className="px-4 py-3">{item.item_code}</td>
                    <td className="px-4 py-3">{item.name}</td>
                    <td className="px-4 py-3 capitalize">{item.category}</td>
                    <td className="px-4 py-3">${(item.price / 100).toFixed(2)}</td>
                    <td className="px-4 py-3">{item.quantity}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs ${
                        item.status === 'in_stock' ? 'bg-green-100 text-green-800' :
                        item.status === 'sold' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => handleEdit(item)}
                        className="text-blue-600 mr-2"
                      >
                        Edit
                      </button>
                      {(user?.role === 'manager' || user?.role === 'owner') && (
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="text-red-600"
                        >
                          Delete
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
