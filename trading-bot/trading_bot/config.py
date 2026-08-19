import os
from dotenv import load_dotenv

load_dotenv()

ANGEL_BASE_URL = os.getenv("ANGEL_BASE_URL", "")
ANGEL_CLIENT_ID = os.getenv("ANGEL_CLIENT_ID", "")
ANGEL_CLIENT_SECRET = os.getenv("ANGEL_CLIENT_SECRET", "")
ANGEL_ACCESS_TOKEN = os.getenv("ANGEL_ACCESS_TOKEN", "")
ANGEL_REFRESH_TOKEN = os.getenv("ANGEL_REFRESH_TOKEN", "")
ANGEL_ACCOUNT_ID = os.getenv("ANGEL_ACCOUNT_ID", "")

PAPER_MODE = os.getenv("PAPER_MODE", "true").lower() in ("1", "true", "yes")
TRADE_SYMBOLS = [s.strip() for s in os.getenv("TRADE_SYMBOLS", "").split(",") if s.strip()]
ORDER_QUANTITY = int(os.getenv("ORDER_QUANTITY", "1"))
MAX_DAILY_LOSS = float(os.getenv("MAX_DAILY_LOSS", "1000"))

# Add any other tuning defaults here
