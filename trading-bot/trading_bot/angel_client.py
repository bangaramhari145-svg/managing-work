import logging
import requests
from .config import ANGEL_BASE_URL, ANGEL_ACCESS_TOKEN, PAPER_MODE

logger = logging.getLogger(__name__)

class AngelClient:
    def __init__(self, base_url=None, access_token=None):
        self.base = (base_url or ANGEL_BASE_URL).rstrip('/')
        self.token = access_token or ANGEL_ACCESS_TOKEN

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get_quote(self, symbol: str) -> dict:
        """Return a dict with at least last_price key. Placeholder endpoint."""
        if PAPER_MODE:
            logger.info(f"[PAPER] get_quote {symbol}")
            return {"last_price": 0.0}
        url = f"{self.base}/market/quote/{symbol}"
        r = requests.get(url, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def place_order(self, symbol: str, qty: int, side: str = "BUY", product: str = "MIS", price: float = None, stoploss: float = None) -> dict:
        """Place an order. In PAPER_MODE only logs and returns a fake order id."""
        if PAPER_MODE:
            logger.info(f"[PAPER] place_order {side} {symbol} qty={qty} price={price} stop={stoploss}")
            return {"status": "paper", "order_id": f"PAPER-{symbol}-{side}"}

        payload = {
            "symbol": symbol,
            "quantity": qty,
            "side": side,
            "product": product,
        }
        if price is not None:
            payload["price"] = price
        if stoploss is not None:
            payload["stopLoss"] = stoploss

        url = f"{self.base}/orders"
        r = requests.post(url, json=payload, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    def refresh_token(self):
        # Placeholder: implement OAuth refresh with ANGEL_CLIENT_SECRET/ID if required by provider
        logger.info("refresh_token called (placeholder)")
        return True
