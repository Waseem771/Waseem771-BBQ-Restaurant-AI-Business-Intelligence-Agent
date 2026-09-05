from app.security import hash_password, verify_password


def test_password_hash_round_trip():
    encoded = hash_password("a long enough password")
    assert encoded != "a long enough password"
    assert verify_password("a long enough password", encoded)
    assert not verify_password("incorrect password", encoded)
