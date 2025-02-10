from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@example.com", "string", 200),
        ("user1@example.com", "string", 409),
        ("user3@example.com", "string", 200),
        ("user", "string", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("user1@example.com", "string", 200),
        ("user2@example.com", "string", 200),
        ("wrong@example.com", "string", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
