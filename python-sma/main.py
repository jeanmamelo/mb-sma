import logging

from src.db.base import Base
from src.db.engine import SessionLocal, engine
from src.services.mb_candle_service import MercadoBitcoinService
from src.services.pair_service import PairService


def init_db():
    Base.metadata.create_all(bind=engine)
    logging.debug("✅ Banco de dados criado com sucesso!")


def run():
    init_db()

    db = SessionLocal()

    symbols = ["BTC-BRL", "ETH-BRL"]

    for symbol in symbols:
        candles = MercadoBitcoinService.get_last_year_candles(symbol)
        try:
            PairService.save_candles(db, symbol, candles)
            PairService.check_missing_days(db, symbol)
            logging.info("✅ Banco de dados populado com sucesso!")
        except Exception as e:
            logging.error(f"❌ Erro ao salvar candles para {symbol}: {e}")
            continue

    db.close()


if __name__ == "__main__":
    run()
