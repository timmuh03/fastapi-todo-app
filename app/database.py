from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



# SQLite = 'sqlite:///./todosapp.db'
# PostgreSQL = "postgresql+psycopg2://postgres:2in1out03@localhost:5432/TodoApplicationDatabase"
# MySQL = "mysql+pymysql://root:2in1out03@127.0.0.1:3306/TodoApplicationDatabase"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:2in1out03@localhost:5432/TodoApplicationDatabase"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) connect_args only for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()