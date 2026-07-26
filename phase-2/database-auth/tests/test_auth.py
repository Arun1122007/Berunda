from datetime import datetime, timedelta, timezone

import jwt as pyjwt
import pytest
from src.auth.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET,
    create_access_token,
    create_refresh_token,
    create_token_pair,
    decode_token,
)
from src.auth.models import TokenPair, UserInfo
from src.auth.password import hash_password, verify_password


def test_hash_password_returns_string():
    hashed = hash_password("testpass")
    assert isinstance(hashed, str)
    assert len(hashed) > 20


def test_verify_password_correct():
    hashed = hash_password("testpass")
    assert verify_password("testpass", hashed) is True


def test_verify_password_incorrect():
    hashed = hash_password("testpass")
    assert verify_password("wrongpass", hashed) is False


def test_different_hashes_for_same_password():
    h1 = hash_password("testpass")
    h2 = hash_password("testpass")
    assert h1 != h2


def test_verify_password_empty_string():
    hashed = hash_password("")
    assert verify_password("", hashed) is True


def test_create_access_token_returns_string():
    user = UserInfo(user_id=1, email="admin@test.com", role="admin")
    token = create_access_token(user)
    assert isinstance(token, str)
    assert len(token) > 20


def test_decode_access_token_contains_correct_payload():
    user = UserInfo(user_id=42, email="user@test.com", role="officer", district_id=1)
    token = create_access_token(user)
    payload = decode_token(token)
    assert payload["sub"] == "42"
    assert payload["email"] == "user@test.com"
    assert payload["role"] == "officer"
    assert payload["district_id"] == 1
    assert payload["type"] == "access"


def test_create_refresh_token_returns_string():
    user = UserInfo(user_id=1, email="admin@test.com", role="admin")
    token = create_refresh_token(user)
    assert isinstance(token, str)
    assert len(token) > 20


def test_decode_refresh_token_contains_type():
    user = UserInfo(user_id=1, email="admin@test.com", role="admin")
    token = create_refresh_token(user)
    payload = decode_token(token)
    assert payload["type"] == "refresh"
    assert payload["sub"] == "1"


def test_decode_token_with_wrong_secret_fails():
    user = UserInfo(user_id=1, email="a@b.com", role="admin")
    token = create_access_token(user)
    with pytest.raises(pyjwt.InvalidSignatureError):
        pyjwt.decode(token, "wrong-secret", algorithms=[JWT_ALGORITHM])


def test_decode_token_with_invalid_algorithm_fails():
    user = UserInfo(user_id=1, email="a@b.com", role="admin")
    token = create_access_token(user)
    with pytest.raises(pyjwt.InvalidAlgorithmError):
        pyjwt.decode(token, JWT_SECRET, algorithms=["HS512"])


def test_expired_token_raises_error():
    payload = {
        "sub": "1",
        "type": "access",
        "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
    }
    token = pyjwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    with pytest.raises(pyjwt.ExpiredSignatureError):
        decode_token(token)


def test_token_expiry_within_tolerance():
    user = UserInfo(user_id=1, email="a@b.com", role="admin")
    token = create_access_token(user)
    payload = decode_token(token)
    exp = payload["exp"]
    expected = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    assert abs(exp - expected.timestamp()) < 5


def test_create_token_pair_has_both_tokens():
    user = UserInfo(user_id=1, email="a@b.com", role="admin")
    pair = create_token_pair(user)
    assert isinstance(pair, TokenPair)
    assert pair.access_token is not None
    assert pair.refresh_token is not None
    assert pair.access_token != pair.refresh_token


def test_decode_malformed_token_raises_error():
    with pytest.raises(pyjwt.PyJWTError):
        decode_token("not.a.token")


def test_token_payload_iat_exists():
    user = UserInfo(user_id=1, email="iat@test.com", role="analyst")
    token = create_access_token(user)
    payload = decode_token(token)
    assert "iat" in payload
    assert isinstance(payload["iat"], (int, float))
