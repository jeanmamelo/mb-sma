import time
from datetime import datetime, timedelta

import requests

from src.constants import API_URL


class MercadoBitcoinService:
    MAX_RETRIES_SECONDS = 5
    BASE_BACKOFF_SECONDS = 2

    @staticmethod
    def fetch_candles(symbol: str, from_ts: int, to_ts: int) -> list[dict]:
        ONE_DAY = "1d"
        params = {"symbol": symbol, "from": from_ts, "to": to_ts, "resolution": ONE_DAY}

        for attempt in range(1, MercadoBitcoinService.MAX_RETRIES_SECONDS + 1):
            try:
                response = requests.get(API_URL, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                closes = data.get("c", [])
                timestamps = data.get("t", [])

                if not closes or not timestamps:
                    raise ValueError("Candles not found in API response.")

                candles = [
                    {"timestamp": datetime.fromtimestamp(ts), "close": float(close)} for ts, close in zip(timestamps, closes)
                ]

                return candles

            except (requests.RequestException, ValueError) as e:
                wait_time = MercadoBitcoinService.BASE_BACKOFF_SECONDS**attempt
                print(f"[Attempt {attempt}] Error: {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)

        raise ValueError("Max retries exceeded. Failed to fetch candles.")

    @staticmethod
    def get_last_year_candles(symbol: str) -> list[dict]:
        now = datetime.now()
        to_ts = int(now.timestamp())
        from_ts = int((now - timedelta(days=365)).timestamp())
        return MercadoBitcoinService.fetch_candles(symbol, from_ts, to_ts)
