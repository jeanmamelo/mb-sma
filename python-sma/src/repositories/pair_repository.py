from src.db.engine import SessionLocal
from src.models.pair import Pair


class PairRepository:
    @staticmethod
    def save_pairs(pairs: list[Pair]) -> None:
        with SessionLocal() as session:
            session.add_all(pairs)
            session.commit()
