from backend.security.tokens import generate_secure_token, hash_token


def test_generate_secure_token_is_non_empty_and_unique():
    first_token = generate_secure_token()
    second_token = generate_secure_token()

    assert first_token
    assert second_token
    assert first_token != second_token


def test_hash_token_returns_deterministic_digest():
    token = "sample-token"

    assert hash_token(token) == hash_token(token)
    assert hash_token(token) != hash_token("different-token")
