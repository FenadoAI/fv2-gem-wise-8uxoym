import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { authApi } from '../api/client';

export default function UsersPage() {
  const { user, logout } = useAuth();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'staff'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await authApi.register(formData);
      setSuccess('User created successfully');
      setShowForm(false);
      setFormData({ username: '', email: '', password: '', role: 'staff' });
    } catch (error) {
      setError(error.response?.data?.detail?.error?.message || 'Failed to create user');
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <Link to="/admin/dashboard" className="text-blue-600">&larr; Dashboard</Link>
              <h1 className="text-2xl font-bold">User Management</h1>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">{user?.username} (Owner)</span>
              <button onClick={logout} className="text-red-600">Logout</button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8">
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
        {success && <div className="bg-green-100 text-green-700 p-3 rounded mb-4">{success}</div>}

        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-semibold">Manage Staff & Managers</h2>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            {showForm ? 'Cancel' : '+ Add New User'}
          </button>
        </div>

        {showForm && (
          <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
            <h3 className="text-lg font-bold mb-4">Create New User</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block font-semibold mb-2">Username</label>
                <input
                  type="text"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={formData.username}
                  onChange={(e) => setFormData({...formData, username: e.target.value})}
                  placeholder="john_doe"
                />
              </div>

              <div>
                <label className="block font-semibold mb-2">Email</label>
                <input
                  type="email"
                  required
                  className="w-full border rounded px-3 py-2"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  placeholder="john@example.com"
                />
              </div>

              <div>
                <label className="block font-semibold mb-2">Password</label>
                <input
                  type="password"
                  required
                  minLength="8"
                  className="w-full border rounded px-3 py-2"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                  placeholder="Min 8 characters"
                />
              </div>

              <div>
                <label className="block font-semibold mb-2">Role</label>
                <select
                  className="w-full border rounded px-3 py-2"
                  value={formData.role}
                  onChange={(e) => setFormData({...formData, role: e.target.value})}
                >
                  <option value="staff">Staff</option>
                  <option value="manager">Manager</option>
                  <option value="owner">Owner</option>
                </select>
                <p className="text-sm text-gray-500 mt-1">
                  Staff: Can manage inventory and view orders<br />
                  Manager: Staff + Can delete items and view reports<br />
                  Owner: Full access including user management
                </p>
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
              >
                Create User
              </button>
            </form>
          </div>
        )}

        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="font-semibold text-lg mb-4">User Roles & Permissions</h3>

          <div className="space-y-4">
            <div className="border-l-4 border-purple-500 pl-4">
              <h4 className="font-bold text-purple-700">Owner</h4>
              <ul className="text-sm text-gray-600 list-disc list-inside">
                <li>Full system access</li>
                <li>Create and manage users</li>
                <li>Delete inventory items</li>
                <li>View all reports</li>
                <li>Manage orders</li>
              </ul>
            </div>

            <div className="border-l-4 border-blue-500 pl-4">
              <h4 className="font-bold text-blue-700">Manager</h4>
              <ul className="text-sm text-gray-600 list-disc list-inside">
                <li>Manage inventory (including delete)</li>
                <li>View and update orders</li>
                <li>Access sales and inventory reports</li>
              </ul>
            </div>

            <div className="border-l-4 border-green-500 pl-4">
              <h4 className="font-bold text-green-700">Staff</h4>
              <ul className="text-sm text-gray-600 list-disc list-inside">
                <li>Add and edit inventory items</li>
                <li>View and update orders</li>
                <li>Cannot delete items or view reports</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}