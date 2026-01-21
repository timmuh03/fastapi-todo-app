import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.routers.auth import bcrypt_context
from app.database import Base, get_db
from app.routers.auth import get_current_user
from app.main import app
from app.models import Users, Todos



SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:2in1out03@localhost:5432/TodoApplicationDatabaseTest"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)



@pytest.fixture(scope="session", autouse=True)
def clean_test_db():
    # each test session should start with a clean database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSessionLocal()

    # Start a SAVEPOINT so commits inside app code don't end outer transaction
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        # If the SAVEPOINT ended, restart it
        if trans.nested and not trans._parent.nested:
            sess.begin_nested()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def test_user(db_session):
    user = Users(
        username='timmuhTEST',
        email='timmuh@TEST.com',
        hashed_password=bcrypt_context.hash("TESTpassword123"),
        role='admin',
        phone_number="(111)-111-1111"
    )    

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_2(db_session):
    user = Users(
        username='timmuhTEST_2',
        email='timmuh@TEST_2.com',
        hashed_password=bcrypt_context.hash("TESTpassword123"),
        role='TEST_2',
        phone_number="(111)-111-1111"
    )    

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def client_unauthenticated(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(db_session, test_user):
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return {'username': test_user.username, 'id': test_user.id, 'user_role': 'admin'}
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_user_2(db_session, test_user_2):
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return {'username': test_user_2.username, 'id': test_user_2.id, 'user_role': 'TEST'}
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_todo(db_session, test_user):
    todo = Todos(
        title = "Learn to code TEST",
        description = "Need to learn everyday TEST",
        priority = 5,
        complete = False,
        owner_id = test_user.id,
    )

    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    return todo

@pytest.fixture(scope="function")
def test_user2_todo(db_session, test_user_2):
    todo = Todos(
        title="TEST__user2s_todo",
        description="TEST__",
        priority=3,
        complete=False,
        owner_id=test_user_2.id
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo
