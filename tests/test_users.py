from fastapi import status

from app.routers.users import bcrypt_context
from app.models import Users





def test_get_user_unauthenticated(client_unauthenticated):
    response = client_unauthenticated.get("/user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user(client, test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data['id'] == test_user.id
    assert data['username'] == test_user.username
    assert data['email'] == test_user.email


def test_change_password(client, test_user, db_session):
    old_hash = test_user.hashed_password

    response = client.put("/user", json={"password": "TESTpassword123",
                                                "new_password": "TESTpassword123new"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated = db_session.query(Users).filter(Users.id == test_user.id).first()
    assert updated.hashed_password != old_hash
    assert bcrypt_context.verify("TESTpassword123new", updated.hashed_password)


def test_change_password_invalid_current_password(client, test_user):
    response = client.put("/user", json={"password": "TESTpassword",
                                                "new_password": "TESTpassword123new"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': "Error on password change"}


def test_update_phone_number_success(client, db_session, test_user):
    response = client.put("/user/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    updated = db_session.query(Users).filter(Users.id == test_user.id)
    assert test_user.phone_number == "2222222222"
