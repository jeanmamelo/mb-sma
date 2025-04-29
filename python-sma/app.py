import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.models.pair import Pair

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mb")
DB_USER = os.getenv("DB_USER", "mb")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mb")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados criado com sucesso!")


def main():
    init_db()

    # Teste: criando um par dummy
    with SessionLocal() as session:
        dummy_pair = Pair(
            pair="BRLBTC",
            timestamp="2024-04-27T00:00:00",
            mms_20=100.5,
            mms_50=105.3,
            mms_200=110.7,
        )
        session.add(dummy_pair)
        session.commit()
    print("✅ Dummy pair adicionado com sucesso!")


if __name__ == "__main__":
    main()
