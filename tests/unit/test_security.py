from app.auth.security import hash_password, verify_password


def test_hash_password():
    password = "mypassword"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_verify_password_wrong():
    password = "mypassword"
    hashed = hash_password(password)

    assert not verify_password("wrongpassword", hashed)