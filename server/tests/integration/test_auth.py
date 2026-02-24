from datetime import datetime, timedelta, timezone
import pytest
import jwt
from sqlalchemy import select
from models.user import User
from core.security import ALGORITHM, SECRET_KEY, create_access_token, create_verification_token, hash_password


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

@pytest.mark.asyncio
async def test_login_success_verified_user(client, db_session):
    password = "correct_password"

    user = User(
        username ="login_user",
        email="login@lab.com",
        password_hash=hash_password(password),
        is_active=True,
        verified_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    await db_session.commit()

    login_payload = {
        "username": "login@lab.com",
        "password": password
    }
    
    response = await client.post("auth/login", data=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_fails_unverified_user(client, db_session):
    # User exists but verified_at is None
    password = "correct_password"
    user = User(
        username="unverified_tester",
        email="unverified@lab.com",
        password_hash=hash_password(password),
        is_active=True, # True but verified_at=None
        verified_at=None
    )

    db_session.add(user)
    await db_session.commit()

    # fill in credential
    response = await client.post("/auth/login", data={
        "username": "unverified@lab.com",
        "password": password
    })

    # assert
    assert response.status_code == 403
    assert "verify" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_login_fails_disabled_account(client, db_session):
    user = User(
        username="disabled_tester",
        email="disabled@lab.com",
        password_hash=hash_password("password"),
        is_active=False  # The "Disabled" gatekeeper
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post("/auth/login", data={
        "username": "disabled@lab.com",
        "password": "password"
    })

    assert response.status_code == 403
    assert "disabled" in response.json()["detail"].lower()
    
@pytest.mark.asyncio
async def test_get_me_success(client, db_session):
    # local Setup
    user = User(
        username="local_tester",
        email="local@test.com",
        password_hash=hash_password("password123"),
        is_active=True,
        verified_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # action
    token = create_access_token(data={"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/auth/me", headers=headers)

    # assert
    assert response.status_code == 200
    assert response.json()["email"] == "local@test.com"

@pytest.mark.asyncio
async def test_get_me_invalid_token(client):
    # pass a garbage token
    headers = {"Authorization": "Bearer not-a-real-token"}
    response = await client.get("/auth/me", headers=headers)

    # should match your credentials_exception
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_me_expired_token(client, db_session):
    # 1. Setup local user
    user = User(
        username="expired_tester",
        email="expired@test.com",
        password_hash=hash_password("password"),
        is_active=True,
        verified_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    await db_session.commit()

    # manually craft an expired token
    expire = datetime.now(timezone.utc) - timedelta(hours=1)
    to_encode = {"sub": str(user.id), "exp": int(expire.timestamp())}
    # Note: Use your SECRET_KEY and ALGORITHM here
    expired_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    headers = {"Authorization": f"Bearer {expired_token}"}
    response = await client.get("/auth/me", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"