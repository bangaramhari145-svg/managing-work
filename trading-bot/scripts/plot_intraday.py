#!/usr/bin/env python
"""Fetch intraday candle data for a given search term and interval and save a PNG chart.
Usage: python trading-bot/scripts/plot_intraday.py <API_KEY> <CLIENT_CODE> <PASSWORD> <TOTP>
Defaults: search term 'NIFTY', exchange 'NFO', interval 'FIVE_MINUTE' (5-min candles for F&O)
"""
import sys
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from SmartApi.smartConnect import SmartConnect

if len(sys.argv) < 5:
    print("Usage: plot_intraday.py <API_KEY> <CLIENT_CODE> <PASSWORD> <TOTP>")
    sys.exit(1)

api_key, client_code, password, totp = sys.argv[1:5]
sc = SmartConnect(api_key=api_key)
res = sc.generateSession(client_code, password, totp)
if not res.get('status'):
    print('Login failed:', res)
    sys.exit(2)

# Search for NIFTY F&O scrip
search = sc.searchScrip('NFO', 'NIFTY')
if not search.get('status') or not search.get('data'):
    print('Search failed or no results:', search)
    sys.exit(3)

# pick first FUT symboltoken
items = search['data']
fut = None
for it in items:
    ts = it.get('tradingsymbol','')
    if 'FUT' in ts or 'FUTURE' in ts or 'FUTURES' in ts:
        fut = it
        break
if not fut:
    # fallback: pick first item
    fut = items[0]

symboltoken_raw = fut['symboltoken']
# sometimes symboltoken contains multiple tokens separated by spaces; pick first
symboltoken = str(symboltoken_raw).split()[0]
tradingsymbol = fut['tradingsymbol']
print(f"Using tradingsymbol={tradingsymbol}, token={symboltoken}")

# prepare date range: today 09:15 to now
today = datetime.now().strftime('%Y-%m-%d')
fromdate = f"{today} 09:15"
todate = datetime.now().strftime('%Y-%m-%d %H:%M')
params = {
    'exchange': 'NFO',
    'symboltoken': symboltoken,
    'interval': 'FIVE_MINUTE',
    'fromdate': fromdate,
    'todate': todate
}

candles = sc.getCandleData(params)
if not candles:
    print('No response from getCandleData')
    sys.exit(4)

# SmartAPI returns list of [timestamp, open, high, low, close, volume] rows in data
data = candles.get('data') if isinstance(candles, dict) else None
if not data:
    print('No candle data returned:', candles)
    sys.exit(4)

# build DataFrame
df = pd.DataFrame(data, columns=['timestamp','open','high','low','close','volume'])
# convert timestamp to datetime
# SmartAPI timestamps may be in epoch ms or string — try to coerce
try:
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
except Exception:
    df['timestamp'] = pd.to_datetime(df['timestamp'])

plt.figure(figsize=(12,6))
plt.plot(df['timestamp'], df['close'], label=f'{tradingsymbol} close')
plt.fill_between(df['timestamp'], df['low'], df['high'], color='lightgray', alpha=0.4)
plt.title(f'{tradingsymbol} 5-min Intraday ({fromdate} to {todate})')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid(True)

outdir = os.path.join('trading-bot','artifacts')
os.makedirs(outdir, exist_ok=True)
outfile = os.path.join(outdir, f'{tradingsymbol}_5min.png')
plt.savefig(outfile)
print('Saved', outfile)
