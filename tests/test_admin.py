from fastapi import status
from app.models import Todos, Users


def test_admin_read_all_not_authorized(client_user_2):
    resp = client_user_2.get("/admin/todo")
    assert resp.status_code == status.HTTP_403_FORBIDDEN

def test_admin_read_all_not_authenticated(client_unauthenticated):
    resp = client_unauthenticated.get("/admin/todo")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED

def test_admin_read_all_todos_authenticated(client, test_todo):
    resp = client.get('/admin/todo')
    assert resp.status_code == status.HTTP_200_OK
    
    data = resp.json()
    assert len(data) == 1
    assert data[0]['id'] == test_todo.id
    assert data[0]['title'] == test_todo.title
    assert data[0]['owner_id'] == test_todo.owner_id

def test_admin_delete_todo(client, db_session, test_todo):
    resp = client.delete(f"/admin/todo/{test_todo.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    model = db_session.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None

def test_admin_delete_todo_not_found(client):
    resp = client.delete("/admin/todo/999999999999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {'detail': 'Todo not found.'}

def test_admin_read_all_users(client, test_user):
    resp = client.get("/admin/users")
    assert resp.status_code == status.HTTP_200_OK
    
    data = resp.json()
    assert len(data) >= 1
    assert any(u['id'] == test_user.id for u in data)
    assert any(u['username'] == test_user.username for u in data)
    assert any(u['email'] == test_user.email for u in data)

def test_admin_delete_user(client, test_user_2, db_session):
    resp = client.delete(f"/admin/user/{test_user_2.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    model = db_session.query(Users).filter(Users.id == test_user_2.id).first()
    assert model is None

def test_admin_delete_user_not_found(client):
    resp = client.delete("/admin/user/999999999999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {'detail': "Invalid user ID."}