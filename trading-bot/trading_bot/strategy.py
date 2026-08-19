import logging
from .config import TRADE_SYMBOLS, ORDER_QUANTITY

logger = logging.getLogger(__name__)

class Strategy:
    """Minimal example strategy. Replace with your logic.

    Behavior:
      - If env var FORCE_TRADE=true or TRADE_SYMBOLS set with a symbol, it returns a simple BUY order request for demo.
      - Real strategies should compute signals from market data here.
    """
    def __init__(self, client):
        self.client = client

    def scan_and_create_orders(self):
        orders = []
        if not TRADE_SYMBOLS:
            logger.info("No TRADE_SYMBOLS configured — nothing to do.")
            return orders
        for s in TRADE_SYMBOLS:
            # Get quote (client returns a dict with last_price in this skeleton)
            q = self.client.get_quote(s)
            price = q.get("last_price") if isinstance(q, dict) else None
            logger.info(f"Quote {s} => {price}")
            # Example signal: if price is available, prepare a very small buy order for demo/testing
            if price is not None:
                orders.append({
                    "symbol": s,
                    "qty": ORDER_QUANTITY,
                    "side": "BUY",
                    "product": "MIS",
                    "price": None,
                    "comment": "demo small order from strategy"
                })
        return orders
