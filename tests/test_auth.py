import pytest

from fastapi import HTTPException, status
from jose import jwt
from datetime import timedelta

from app.routers.auth import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from app.database import get_db



def test_authenticate_user(db_session, test_user):
    authenticated_user = authenticate_user(test_user.username, "TESTpassword123", db_session)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    unauthenticated_user = authenticate_user("UnauthenticatedUser", "TESTpassword123", db_session)
    assert unauthenticated_user is False

    wrong_password_user = authenticate_user(test_user.username, "TESTwrongpassword123", db_session)
    assert wrong_password_user is False


def test_create_acess_token(test_user_2):
    expires_delta = timedelta(days=1)

    token = create_access_token(test_user_2.username, test_user_2.id, test_user_2.role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM], options={"verify_signature": False})
    assert decoded_token['sub'] == test_user_2.username
    assert decoded_token['id'] == test_user_2.id
    assert decoded_token['role'] == test_user_2.role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not validate user."