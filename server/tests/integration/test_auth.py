import pytest

@pytest.mark.asyncio
async def test_register_duplicate_user_and_email(client):
    # 1. Setup: Register the first user
    payload = {
        "username": "unique_user",
        "email": "unique@lab.com",
        "password": "securepassword123"
    }
    await client.post("/auth/register", json=payload)

    # 2. Action: Try to register with the exact same data
    response = await client.post("/auth/register", json=payload)
    
    # 3. Assertions
    assert response.status_code == 400
    errors = response.json()["detail"]
    
    # Check that BOTH specific errors are present in the list
    assert any("Email is already registered" in err for err in errors)
    assert any("Username is already taken" in err for err in errors)





