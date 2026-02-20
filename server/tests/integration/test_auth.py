import pytest
from sqlalchemy import select
from models.user import User
from core.security import create_verification_token, hash_password

@pytest.mark.asyncio
async def test_register_user_initial_state(client, db_session):
    payload = {
        "username": "new_unique_user",
        "email": "new_unique@lab.com",
        "password": "securepassword123"
    }
    response  = await client.post("/auth/register", json=payload)

    query = select(User).where(User.email == "new_unique@lab.com")

    assert response.status_code == 201

    query = select(User).where(User.email == "new_unique@lab.com")
    result = await db_session.execute(query)
    user = result.scalar_one()

    assert user.is_active == False
    assert user.verified_at == None

@pytest.mark.asyncio
async def test_register_duplicate_user_and_email(client):
    # 1. Setup: Register the first user
    payload = {
        "username": "unique_user",
        "email": "unique@lab.com",
        "password": "securepassword123"
    }
    
    # 2. Action: Try to register with the exact same data
    response = await client.post("/auth/register", json=payload)
    

    response = await client.post("/auth/register", json=payload)
    # 3. Assertions
    assert response.status_code == 400
    errors = response.json()["detail"]
    
    # Check that BOTH specific errors are present in the list
    assert any("Email is already registered" in err for err in errors)
    assert any("Username is already taken" in err for err in errors)


@pytest.mark.asyncio
async def test_verify_email_success(client, db_session):
    test_user = User(
        username = "verify_test",
        email = "verify@lab.com",
        password_hash=hash_password("password123"),
        is_active = False
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    token = create_verification_token(test_user.id)

    response = await client.get(f"/auth/verify-email?token={token}")
    
    assert response.status_code == 200
    assert "verified successfully" in response.json()["message"]

    await db_session.refresh(test_user)
    assert test_user.is_active is True
    assert test_user.verified_at is not None

@pytest.mark.asyncio
async def test_email_invalid_token(client):
    response = await client.get("/auth/verify-email?token=not-a-real-jwt-token")
    assert response.status_code == 400
    assert "Invalid or expired verification link." in response.json()["detail"]


