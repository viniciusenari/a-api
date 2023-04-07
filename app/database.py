from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.user_models import User

engine = create_engine("postgresql://postgres:postgres@localhost:5432/mydb")
Session = sessionmaker(bind=engine)


def test_db_connection():
    try:
        session = Session()
        session.query(User).first()
        return "Connection successful"
    except Exception as e:
        return ("Connection failed:", str(e))


if __name__ == "__main__":
    test_db_connection()
