import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_create_location_success(client: AsyncClient):
    payload = {
        "building": "Biotech Complex",
        "room": "Room 401",
        "area_description": "Mass Spectrometry Lab",
        "notes": "Access code required"
    }
    
    response = await client.post("/location/create", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["building"] == "Biotech Complex"
    assert data["room"] == "Room 401"
    assert data["area_description"] == "Mass Spectrometry Lab"
    assert data["notes"] == "Access code required"
    assert data["is_active"] is True

async def test_create_duplicate_location_fails(client: AsyncClient):
    payload = {"building": "Chemistry Hall", "room": "101"}

    await client.post("/location/create", json=payload)

    response = await client.post("/location/create", json=payload)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

async def test_read_locations_filter_inactive(client: AsyncClient):
    loc_a = await client.post("/location/create", json={"building": "Wing A", "room": "100"})
    loc_a_id = loc_a.json()["id"]

    loc_b = await client.post("/location/create", json={"building": "Wing B", "room": "200"})
    loc_b_id = loc_b.json()["id"]

    await client.delete(f"/location/{loc_b_id}")

    response = await client.get("/location/list")
    assert response.status_code == 200
    active_room = [loc["room"] for loc in response.json()]
    assert "100" in active_room
    assert "200" not in active_room

    response_all = await client.get("/location/list?include_inactive=true")
    assert response_all.status_code == 200
    all_rooms = [loc["room"] for loc in response_all.json()]
    assert "100" in all_rooms
    assert "200" in all_rooms