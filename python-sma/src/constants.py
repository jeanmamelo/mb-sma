import os

API_URL = os.environ.get("API_URL", "https://api.mercadobitcoin.net/api/v4/candles")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mb")
DB_USER = os.getenv("DB_USER", "mb")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mb")
