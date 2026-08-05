from backend.security.passwords import hash_password, verify_password


def test_hash_and_verify_password():
    password = "VeryStrongPassword!123"
    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("wrong-password", password_hash) is False
