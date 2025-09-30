"""
Test jewellery store API endpoints.
Requires server running on port 8001.
Run with: python -m pytest tests/test_jewellery_api.py -v
"""

import os
import sys
import time
from datetime import datetime

import pytest
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

API_BASE = "http://localhost:8001/api"


class TestJewelleryStoreAPI:
    """Test jewellery store management system APIs."""

    # Class-level tokens and IDs to share across tests
    owner_token = None
    staff_token = None
    item_id = None
    order_id = None
    staff_email = None

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data."""
        # Use class-level attributes for persistence across tests
        pass

    def test_01_create_owner_account(self):
        """Test creating owner account (bootstrap test)."""
        # First, create owner via direct DB or login with existing
        # For testing, we'll create an owner account directly via register endpoint
        # This requires bypassing auth for first owner creation

        # Try to login first to see if owner exists
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={"email": "owner@jewelcraft.com", "password": "OwnerPass123"}
        )

        if response.status_code == 200:
            data = response.json()
            assert "token" in data
            assert data["user"]["role"] == "owner"
            self.owner_token = data["token"]
            print(f"✓ Logged in as existing owner: {data['user']['email']}")
        else:
            # Need to create owner account manually or through bootstrap
            print("✗ Owner account doesn't exist. Creating via manual DB insert...")
            # For this test, we'll assume owner exists or needs manual creation
            pytest.skip("Owner account needs to be created first")

    def test_02_register_staff_user(self):
        """Test registering a staff user (owner only)."""
        # Check if already registered
        if TestJewelleryStoreAPI.staff_token:
            print(f"✓ Using existing staff token")
            return

        # Login as owner first
        owner_login = requests.post(
            f"{API_BASE}/auth/login",
            json={"email": "owner@jewelcraft.com", "password": "OwnerPass123"}
        )
        assert owner_login.status_code == 200, "Owner login failed"
        TestJewelleryStoreAPI.owner_token = owner_login.json()["token"]

        # Register staff with unique email
        timestamp = int(time.time() * 1000)  # More granular timestamp
        TestJewelleryStoreAPI.staff_email = f"staff_{timestamp}@test.com"

        response = requests.post(
            f"{API_BASE}/auth/register",
            json={
                "username": f"staff_{timestamp}",
                "email": TestJewelleryStoreAPI.staff_email,
                "password": "StaffPass123",
                "role": "staff"
            },
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.owner_token}"}
        )

        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert "token" in data
        assert data["user"]["role"] == "staff"
        assert data["user"]["email"] == TestJewelleryStoreAPI.staff_email
        TestJewelleryStoreAPI.staff_token = data["token"]
        print(f"✓ Staff user registered: {data['user']['email']}")

    def test_03_staff_login(self):
        """Test staff login."""
        # First ensure staff account exists
        if not TestJewelleryStoreAPI.staff_token:
            self.test_02_register_staff_user()

        # Now login
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={"email": TestJewelleryStoreAPI.staff_email, "password": "StaffPass123"}
        )

        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "token" in data
        assert data["user"]["role"] == "staff"
        print(f"✓ Staff logged in successfully")

    def test_04_add_inventory_item(self):
        """Test adding a jewellery item (staff+)."""
        # Login as staff
        if not TestJewelleryStoreAPI.staff_token:
            self.test_02_register_staff_user()

        # Add item
        item_code = f"JWL-{int(time.time() * 1000)}"
        response = requests.post(
            f"{API_BASE}/inventory",
            json={
                "item_code": item_code,
                "name": "Diamond Ring",
                "description": "Beautiful diamond ring with 18k gold band",
                "category": "ring",
                "price": 250000,  # $2,500.00
                "weight": 5.5,
                "metal_type": "gold",
                "stones": "Diamond 0.5ct",
                "images": ["https://example.com/ring1.jpg"],
                "quantity": 10,
                "status": "in_stock"
            },
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["item_code"] == item_code
        assert data["name"] == "Diamond Ring"
        assert data["price"] == 250000
        TestJewelleryStoreAPI.item_id = data["id"]
        print(f"✓ Inventory item added: {item_code}")

    def test_05_duplicate_item_code(self):
        """Test that duplicate item codes are rejected."""
        if not TestJewelleryStoreAPI.staff_token or not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        # Get the item code
        get_response = requests.get(
            f"{API_BASE}/inventory/{TestJewelleryStoreAPI.item_id}",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )
        item_code = get_response.json()["item_code"]

        # Try to add duplicate
        response = requests.post(
            f"{API_BASE}/inventory",
            json={
                "item_code": item_code,  # Same code
                "name": "Another Ring",
                "description": "Test duplicate",
                "category": "ring",
                "price": 100000,
                "weight": 3.0,
                "metal_type": "silver",
                "images": ["https://example.com/ring2.jpg"],
                "quantity": 5,
                "status": "in_stock"
            },
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 409, f"Expected 409 conflict, got {response.status_code}"
        assert "DUPLICATE_ITEM_CODE" in response.text
        print(f"✓ Duplicate item code rejected correctly")

    def test_06_get_inventory(self):
        """Test getting inventory list (staff+)."""
        if not TestJewelleryStoreAPI.staff_token:
            self.test_02_register_staff_user()

        response = requests.get(
            f"{API_BASE}/inventory",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert isinstance(data["items"], list)
        print(f"✓ Inventory retrieved: {data['total']} total items")

    def test_07_update_inventory_item(self):
        """Test updating a jewellery item (staff+)."""
        if not TestJewelleryStoreAPI.staff_token or not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        response = requests.patch(
            f"{API_BASE}/inventory/{TestJewelleryStoreAPI.item_id}",
            json={
                "price": 300000,  # Update price to $3,000
                "quantity": 8  # Update quantity
            },
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["price"] == 300000
        assert data["quantity"] == 8
        print(f"✓ Inventory item updated successfully")

    def test_08_public_catalog_access(self):
        """Test public catalog access (no auth required)."""
        # Ensure there's at least one item
        if not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        response = requests.get(f"{API_BASE}/catalog")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)
        # Should only show in_stock items
        for item in data["items"]:
            assert item["status"] == "in_stock"
        print(f"✓ Public catalog accessible: {len(data['items'])} in-stock items")

    def test_09_get_catalog_item(self):
        """Test getting single catalog item (public)."""
        if not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        response = requests.get(f"{API_BASE}/catalog/{TestJewelleryStoreAPI.item_id}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == TestJewelleryStoreAPI.item_id
        assert data["status"] == "in_stock"
        print(f"✓ Catalog item retrieved: {data['name']}")

    def test_10_place_order(self):
        """Test placing a COD order (public)."""
        if not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        response = requests.post(
            f"{API_BASE}/orders",
            json={
                "customer_name": "John Doe",
                "customer_email": "john@example.com",
                "customer_phone": "1234567890",
                "items": [
                    {"item_id": TestJewelleryStoreAPI.item_id, "quantity": 2}
                ],
                "shipping_address": {
                    "line1": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001",
                    "country": "USA"
                },
                "notes": "Please deliver between 9 AM - 5 PM"
            }
        )

        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["customer_name"] == "John Doe"
        assert data["payment_method"] == "cod"
        assert data["status"] == "pending"
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 2
        TestJewelleryStoreAPI.order_id = data["id"]
        print(f"✓ Order placed: {data['id']} for ${data['total_amount']/100:.2f}")

    def test_11_order_reduces_inventory(self):
        """Test that placing an order reduces inventory quantity."""
        # Get initial quantity
        if not TestJewelleryStoreAPI.staff_token or not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        initial_response = requests.get(
            f"{API_BASE}/inventory/{TestJewelleryStoreAPI.item_id}",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )
        initial_qty = initial_response.json()["quantity"]

        # Place order for 1 item
        order_response = requests.post(
            f"{API_BASE}/orders",
            json={
                "customer_name": "Jane Smith",
                "customer_email": "jane@example.com",
                "customer_phone": "9876543210",
                "items": [{"item_id": TestJewelleryStoreAPI.item_id, "quantity": 1}],
                "shipping_address": {
                    "line1": "456 Oak Ave",
                    "city": "Boston",
                    "state": "MA",
                    "zip": "02101",
                    "country": "USA"
                }
            }
        )
        assert order_response.status_code == 201

        # Check quantity reduced
        final_response = requests.get(
            f"{API_BASE}/inventory/{TestJewelleryStoreAPI.item_id}",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )
        final_qty = final_response.json()["quantity"]

        assert final_qty == initial_qty - 1, f"Expected {initial_qty - 1}, got {final_qty}"
        print(f"✓ Inventory reduced correctly: {initial_qty} → {final_qty}")

    def test_12_get_orders_staff(self):
        """Test getting orders list (staff+)."""
        if not TestJewelleryStoreAPI.staff_token:
            self.test_02_register_staff_user()

        response = requests.get(
            f"{API_BASE}/orders",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "orders" in data
        assert isinstance(data["orders"], list)
        print(f"✓ Orders retrieved: {data['total']} total orders")

    def test_13_get_single_order(self):
        """Test getting single order details (staff+)."""
        if not TestJewelleryStoreAPI.staff_token or not TestJewelleryStoreAPI.order_id:
            self.test_10_place_order()
            if not TestJewelleryStoreAPI.staff_token:
                self.test_02_register_staff_user()

        response = requests.get(
            f"{API_BASE}/orders/{TestJewelleryStoreAPI.order_id}",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == TestJewelleryStoreAPI.order_id
        print(f"✓ Order details retrieved: {data['customer_name']}")

    def test_14_update_order_status(self):
        """Test updating order status (staff+)."""
        if not TestJewelleryStoreAPI.staff_token or not TestJewelleryStoreAPI.order_id:
            self.test_10_place_order()
            if not TestJewelleryStoreAPI.staff_token:
                self.test_02_register_staff_user()

        response = requests.patch(
            f"{API_BASE}/orders/{TestJewelleryStoreAPI.order_id}/status",
            json={
                "status": "confirmed",
                "notes": "Order confirmed by staff"
            },
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["status"] == "confirmed"
        print(f"✓ Order status updated: {data['status']}")

    def test_15_insufficient_stock_error(self):
        """Test that ordering more than available stock is rejected."""
        if not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        # Try to order 1000 items (more than stock)
        response = requests.post(
            f"{API_BASE}/orders",
            json={
                "customer_name": "Test User",
                "customer_email": "test@example.com",
                "customer_phone": "5555555555",
                "items": [{"item_id": TestJewelleryStoreAPI.item_id, "quantity": 1000}],
                "shipping_address": {
                    "line1": "789 Elm St",
                    "city": "Chicago",
                    "state": "IL",
                    "zip": "60601",
                    "country": "USA"
                }
            }
        )

        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        assert "INSUFFICIENT_STOCK" in response.text
        print(f"✓ Insufficient stock error handled correctly")

    def test_16_unauthorized_access(self):
        """Test that endpoints requiring auth reject unauthenticated requests."""
        response = requests.get(f"{API_BASE}/inventory")

        # FastAPI's HTTPBearer returns 403 when no credentials provided, 401 when invalid
        assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
        print(f"✓ Unauthorized access rejected (status {response.status_code})")

    def test_17_catalog_filtering(self):
        """Test catalog filtering by category."""
        response = requests.get(f"{API_BASE}/catalog?category=ring&limit=10")

        assert response.status_code == 200
        data = response.json()
        # All items should be rings
        for item in data["items"]:
            assert item["category"] == "ring"
        print(f"✓ Catalog filtering works: {len(data['items'])} rings found")

    def test_18_search_functionality(self):
        """Test search in catalog."""
        if not TestJewelleryStoreAPI.item_id:
            self.test_04_add_inventory_item()

        response = requests.get(f"{API_BASE}/catalog?search=diamond")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["items"], list)
        # Should find items with 'diamond' in name/description
        print(f"✓ Search functionality works: {len(data['items'])} items found")

    def test_19_pagination(self):
        """Test pagination in catalog."""
        response = requests.get(f"{API_BASE}/catalog?page=1&limit=5")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert "total_pages" in data
        assert len(data["items"]) <= 5
        print(f"✓ Pagination works: Page {data['page']} of {data['total_pages']}")

    def test_20_get_current_user(self):
        """Test getting current user info."""
        if not TestJewelleryStoreAPI.staff_token:
            self.test_02_register_staff_user()

        response = requests.get(
            f"{API_BASE}/auth/me",
            headers={"Authorization": f"Bearer {TestJewelleryStoreAPI.staff_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == TestJewelleryStoreAPI.staff_email
        assert data["role"] == "staff"
        print(f"✓ Current user info retrieved: {data['username']}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("JEWELLERY STORE API TESTS")
    print("="*60)
    print("Server must be running on http://localhost:8001")
    print("="*60 + "\n")

    # Run tests
    pytest.main([__file__, "-v", "-s"])