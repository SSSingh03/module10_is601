import pytest
from fastapi import HTTPException

from app.auth.dependencies import get_current_user, get_current_active_user
from app.schemas.user import UserRead


class DummyUser:
    def __init__(self, id=1, email="test@example.com"):
        self.id = id
        self.email = email


def test_get_current_user_valid(monkeypatch):
    """Test valid user retrieval"""

    # Mock token verification
    def mock_verify_token(token):
        return 1

    # Mock database query
    class MockQuery:
        def filter(self, *args, **kwargs):
            return self

        def first(self):
            return DummyUser()

    class MockDB:
        def query(self, model):
            return MockQuery()

    from app.models.user import User
    monkeypatch.setattr(User, "verify_token", mock_verify_token)

    db = MockDB()
    user = get_current_user(db=db, token="valid_token")

    assert isinstance(user, UserRead)
    assert user.id == 1


def test_get_current_user_invalid_token(monkeypatch):
    """Test invalid token"""

    def mock_verify_token(token):
        return None

    from app.models.user import User
    monkeypatch.setattr(User, "verify_token", mock_verify_token)

    class MockDB:
        def query(self, model):
            return None

    db = MockDB()

    with pytest.raises(HTTPException):
        get_current_user(db=db, token="invalid_token")


def test_get_current_user_user_not_found(monkeypatch):
    """Test token valid but user not found"""

    def mock_verify_token(token):
        return 1

    class MockQuery:
        def filter(self, *args, **kwargs):
            return self

        def first(self):
            return None

    class MockDB:
        def query(self, model):
            return MockQuery()

    from app.models.user import User
    monkeypatch.setattr(User, "verify_token", mock_verify_token)

    db = MockDB()

    with pytest.raises(HTTPException):
        get_current_user(db=db, token="valid_token")


def test_get_current_active_user():
    """Test active user dependency"""

    user = UserRead(id=1, email="test@example.com")

    active_user = get_current_active_user(current_user=user)

    assert active_user == user