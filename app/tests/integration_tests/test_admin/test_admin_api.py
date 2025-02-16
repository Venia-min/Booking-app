import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_logout(ac: AsyncClient):
    pass
    # response = await ac.post(
    #     "/admin/login",
    #     json={"username": "user@example.com", "password": "string"},
    # )
    # assert response.status_code == 200
    # assert "booking_access_token" in ac.cookies
    #
    # response = await ac.post("/admin/logout")
    # assert response.status_code == 200
    # assert "booking_access_token" not in ac.cookies
