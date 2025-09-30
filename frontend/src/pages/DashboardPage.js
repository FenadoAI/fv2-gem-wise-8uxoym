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
