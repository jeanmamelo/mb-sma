import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.models.pair import Pair
from src.services.sma_service import SMAService


class PairService:
    @staticmethod
    def save_candles(db: Session, symbol: str, candles: list[dict]) -> None:
        candles.sort(key=lambda x: x["timestamp"])

        closes = [candle["close"] for candle in candles]

        mms_20_values = SMAService.calculate_simple_moving_average(closes, 20)
        mms_50_values = SMAService.calculate_simple_moving_average(closes, 50)
        mms_200_values = SMAService.calculate_simple_moving_average(closes, 200)

        for i, candle in enumerate(candles):
            stmt = insert(Pair).values(
                pair=symbol,
                timestamp=candle["timestamp"],
                mms_20=mms_20_values[i] if i < len(mms_20_values) else None,
                mms_50=mms_50_values[i] if i < len(mms_50_values) else None,
                mms_200=mms_200_values[i] if i < len(mms_200_values) else None,
            )
            stmt = stmt.on_conflict_do_nothing(index_elements=["timestamp", "pair"])
            db.execute(stmt)

        db.commit()

    @staticmethod
    def check_missing_days(db: Session, symbol: str) -> bool:
        from datetime import datetime, timedelta

        now = datetime.now()
        one_year_ago = now - timedelta(days=365)

        records = (
            db.query(Pair)
            .filter(Pair.pair == symbol, Pair.timestamp >= one_year_ago, Pair.timestamp <= now)
            .order_by(Pair.timestamp)
            .all()
        )

        expected_days = set((one_year_ago + timedelta(days=i)).date() for i in range(366))
        actual_days = set(record.timestamp.date() for record in records)

        missing_days = expected_days - actual_days

        if missing_days:
            logging.warning(f"🚨 ALERTA: Faltando dias para {symbol}: {missing_days}")
            return True

        return False
