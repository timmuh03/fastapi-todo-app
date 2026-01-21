from fastapi import status
from app.models import Todos



def test_read_all_authenticated(test_todo, client):
    response = client.get("/todos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) == 1
    assert data[0]['title'] == 'Learn to code TEST'
    assert data[0]['owner_id'] == test_todo.owner_id

def test_read_all_filtered(test_todo, test_user2_todo, client):
    resp = client.get("/todos/")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()

    assert len(data) == 1
    assert data[0]['id'] == test_todo.id


def test_read_one_authenticated(test_todo, client):
    response = client.get(f"/todos/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["owner_id"] == test_todo.owner_id
    assert isinstance(data["complete"], bool)
    assert 1 <= data['priority'] <= 5, f"Invalid priority: {data['priority']}"

def test_read_one_forbidden_user(test_todo, client_user_2):
    resp = client_user_2.get(f"/todo/{test_todo.id}")

    assert resp.status_code == status.HTTP_404_NOT_FOUND

def test_read_one_notfound(client):
    resp = client.get("/todos/9999999999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {'detail': 'ID not found.'}

def test_create_todo(client):
    request_data = {
        'title': 'TEST__New Todo!',
        'description': 'TEST__ New todo description.',
        'priority': 5,
        'complete': False
    }

    response = client.post('/todos/', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data['title']  == request_data['title']
    assert data['description']  == request_data['description']
    assert data['priority']  == request_data['priority']
    assert data['complete']  == request_data['complete']
    assert 'id' in data
    assert 'owner_id' in data

def test_update_todo(client, test_todo):
    payload = {
        'title': 'TEST__ Change the title of the todo already saved!',
        'description': 'TEST__ Need to learn everyday!',
        'priority': 5,
        'complete': False
    }

    resp = client.put(f'/todos/{test_todo.id}', json=payload)
    assert resp.status_code == status.HTTP_200_OK
    
    data = resp.json()
    assert data['title'] == 'TEST__ Change the title of the todo already saved!'

def test_update_todo_not_found(client):
    payload = {
        'title': 'TEST__ Change the title of the todo already saved!',
        'description': 'TEST__ Need to learn everyday!',
        'priority': 5,
        'complete': False
    }

    resp = client.put(f'/todos/99999999999', json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {'detail': 'Todo ID not found'}

def test_delete_todo(client, test_todo, db_session):
    resp = client.delete(f'/todos/{test_todo.id}')
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    model = db_session.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None
    
def test_delete_todo_not_found(client, test_todo, db_session):
    resp = client.delete(f'/todos/9999999999')
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {'detail': 'Todo ID not found'}