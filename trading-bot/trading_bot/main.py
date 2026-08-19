import logging
import argparse
import time
from .angel_client import AngelClient
from .strategy import Strategy
from .config import PAPER_MODE

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def run_once():
    client = AngelClient()
    strat = Strategy(client)
    orders = strat.scan_and_create_orders()
    for o in orders:
        logging.info(f"Placing order: {o}")
        resp = client.place_order(o["symbol"], o["qty"], side=o.get("side","BUY"), product=o.get("product","MIS"), price=o.get("price"))
        logging.info(f"Order response: {resp}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run a single scan and exit")
    parser.add_argument("--loop", action="store_true", help="Loop every N seconds")
    parser.add_argument("--interval", type=int, default=60, help="Loop interval seconds")
    args = parser.parse_args()

    logging.info(f"Starting trading-bot (PAPER_MODE={PAPER_MODE})")
    if args.once:
        run_once()
        return

    if args.loop:
        try:
            while True:
                run_once()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            logging.info("Stopped by user")

if __name__ == '__main__':
    main()
