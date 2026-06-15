import pytest
from httpx import AsyncClient

# mark all tests in this file as async
pytestmark = pytest.mark.asyncio

async def test_create_vendor(client: AsyncClient):
    payload = {
        "company_name": "Test Vendor Alpha",
        "contact_person": "Vendor Test Vendorov",
        "email": "vendor@test.com",
        "phone": "123-456-7890",
        "address": "str. Vendor 10",
        "specialties": "Vendor's test specialties",
    }

    response = await client.post("/vendor/create", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["company_name"] == "Test Vendor Alpha"
    assert data["contact_person"] == "Vendor Test Vendorov"
    assert data["email"] == "vendor@test.com"
    assert data[ "phone"] == "123-456-7890"
    assert data["address"] == "str. Vendor 10"
    assert data["specialties"] == "Vendor's test specialties"
    assert data["is_active"] is True
    assert "id" in data

async def test_create_duplicate_vendor_fails(client: AsyncClient):
    payload = {"company_name": "Duplicate Vendor", "email": "dup@test.com"}

    await client.post("/vendor/create", json=payload)

    # creating again same vendor
    response = await client.post("/vendor/create", json=payload)

    assert response.status_code == 400
    assert "is already registered" in response.json()["detail"]

async def test_read_vendors(client: AsyncClient):
    
    await client.post("/vendor/create", json={"company_name": "List Vendor", "email": "list@test.com"})

    response = await client.get("/vendor/list")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["company_name"] is not None

async def test_update_vendor(client: AsyncClient):
    create_resp = await client.post("/vendor/create", json={"company_name": "Old name", "email": "old@test.com"})

    if create_resp.status_code == 422:
            print("FAILED AT CREATION:", create_resp.json())

    vendor_id = create_resp.json()["id"]

    update_payload = {"company_name": "New name"}
    response = await client.patch(f"/vendor/{vendor_id}", json=update_payload)

    if response.status_code == 422:
            print("FAILED AT UPDATE:", response.json())

    assert response.status_code == 200
    data=response.json()

    assert data["company_name"] == "New name"
    assert data["email"] == "old@test.com"

async def test_soft_delete_vendor(client:AsyncClient):
    creat_resp = await client.post("/vendor/create", json={"company_name": "Doomed vendor", "email": "doom@test.com"})
    vendor_id = creat_resp.json()["id"]

    delete_resp = await client.delete(f"/vendor/{vendor_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["is_active"] == False

    list_resp = await client.get("/vendor/list")
    active_vendors = [v["company_name"] for v in list_resp.json()]
    assert "Doomed vendor" not in active_vendors

    history_resp = await client.get("/vendor/list?include_inactive=true")
    hostory_vendors = [v["company_name"] for v in history_resp.json()]
    assert "Doomed vendor" in hostory_vendors
