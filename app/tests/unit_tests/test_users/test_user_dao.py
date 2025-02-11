import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "id, email",
    [
        (1, "user@example.com"),
        (2, "user2@example.com"),
    ],
)
async def test_find_user_by_id(id, email):
    user = await UserDAO.find_by_id(id)

    assert user.id == id
    assert user.email == email
