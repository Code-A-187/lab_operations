import uuid

import pytest

from datetime import datetime, timezone
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from core.security import hash_password, create_access_token

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def auth_headers(db_session: AsyncSession) -> dict:

    unique_suffix = uuid.uuid4().hex[:6]

    user = User(
        username=f"equipment_tester_{unique_suffix}",
        email=f"eq_test_{unique_suffix}@lab.com",
        password_hash=hash_password("securepassword123"),
        is_active = True,
        verified_at = datetime.now(timezone.utc)
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}

async def test_create_equipment_with_nested_response(client: AsyncClient, db_session: AsyncSession, auth_headers: dict):
    from models.vendor import Vendor
    from models.location import Location

    vendor = Vendor(company_name="Eppendorf", email="infor@eppendorf.com", is_active=True)
    location = Location(building="Main Lab", room="Lab 202", is_active=True)
    db_session.add_all([vendor, location])
    await db_session.commit()
    await db_session.refresh(vendor)
    await db_session.refresh(location)

    payload = {
        "model": "Mastercycler X50",
        "serial_number": "EP-998811",
        "vendor_id": vendor.id,
        "location_id": location.id,
        "status": "available",
        "notes": "PCR Machine"
    }

    response = await client.post("/equipment/create", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()

    assert data["serial_number"] == "EP-998811"
    assert data["vendor"]["company_name"] == "Eppendorf"
    assert data["location"]["room"] == "Lab 202"

async def test_create_euqipment_inactive_location_fails(client: AsyncClient, db_session: AsyncSession, auth_headers: dict):
    from models.vendor import Vendor
    from models.location import Location
    vendor = Vendor(company_name="Test Vendor B.V.", email="test@vendor.com", is_active=True)

    location = Location(building="Old Shed", room="Storage B", is_active=False)

    db_session.add_all([vendor, location])
    await db_session.commit()
    await db_session.refresh(vendor)
    await db_session.refresh(location)
    
    payload = {
        "model": "Vortex Mixer",
        "serial_number": "VM-5544",
        "vendor_id": vendor.id,
        "location_id": location.id,
    }

    response = await client.post("/equipment/create", json=payload, headers=auth_headers)
    
    assert response.status_code == 404
    assert "location is invalid or inactive" in response.json()["detail"]

async def test_equipment_unauthorized_fails(client: AsyncClient):
    """test creating equipment without a token is strictly blocked."""
    payload = {"model": "Unauthorized Gear", "serial_number": "BAD-TOKEN-1"}
    
    response = await client.post("/equipment/create", json=payload) # No headers passed
    assert response.status_code == 401