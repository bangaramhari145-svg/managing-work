#!/usr/bin/env python
"""Run live scans for NIFTY futures using saved tokens (expects env vars):
- ANGEL_CLIENT_ID (api key)
- ANGEL_ACCESS_TOKEN
- ANGEL_REFRESH_TOKEN
- ANGEL_ACCOUNT_ID

Produces charts and a ranked list by combined score.
"""
import os
import sys
from SmartApi.smartConnect import SmartConnect
from datetime import datetime
import pandas as pd
from trading_bot.analysis import compute_indicators, score_indicator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

API_KEY = os.getenv('ANGEL_CLIENT_ID')
ACCESS = os.getenv('ANGEL_ACCESS_TOKEN')
REFRESH = os.getenv('ANGEL_REFRESH_TOKEN')
ACCOUNT = os.getenv('ANGEL_ACCOUNT_ID')
if not API_KEY or not ACCESS:
    print('Set ANGEL_CLIENT_ID and ANGEL_ACCESS_TOKEN in environment or GitHub Secrets')
    sys.exit(1)

sc = SmartConnect(api_key=API_KEY)
# set tokens if available
try:
    if ACCESS:
        sc.setAccessToken(ACCESS)
    if REFRESH:
        sc.setRefreshToken(REFRESH)
    if ACCOUNT:
        sc.setUserId(ACCOUNT)
except Exception:
    pass

# search futures
search = sc.searchScrip('NFO', 'NIFTY')
items = search.get('data', []) if isinstance(search, dict) else []
futs = [it for it in items if 'FUT' in it.get('tradingsymbol','')]
if not futs:
    print('No FUT symbols found')
    sys.exit(2)

# pick nearest 3
chosen = futs[:3]
results = []
for fut in chosen:
    token = str(fut['symboltoken']).split()[0]
    ts = fut['tradingsymbol']
    today = datetime.now().strftime('%Y-%m-%d')
    params = {'exchange':'NFO','symboltoken':token,'interval':'FIVE_MINUTE','fromdate':f"{today} 09:15", 'todate':datetime.now().strftime('%Y-%m-%d %H:%M')}
    c = sc.getCandleData(params)
    data = c.get('data') if isinstance(c, dict) else None
    if not data:
        continue
    df = pd.DataFrame(data, columns=['timestamp','open','high','low','close','volume'])
    # coerce
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    ind = compute_indicators(df)
    score = score_indicator(ind)
    results.append({'symbol': ts, 'token': token, 'ind': ind, 'score': score, 'df': df})

ranked = sorted(results, key=lambda x: x['score'], reverse=True)
print('Ranking:')
for r in ranked:
    ind = r['ind']
    print(f"{r['symbol']} score={r['score']:.1f} mom={ind['momentum']:.6f} vol={int(ind['volume'])} ma={ind['ma_signal']} rsi={ind['rsi']:.1f}")

# save charts
outdir = os.path.join('trading-bot','artifacts')
os.makedirs(outdir, exist_ok=True)
for r in ranked:
    df = r['df']
    plt.figure(figsize=(10,6))
    plt.plot(pd.to_datetime(df['timestamp'], unit='ms'), df['close'], label='close')
    df = df.reset_index(drop=True)
    # add simple ma lines
    df['ma5'] = df['close'].rolling(5,min_periods=1).mean()
    df['ma20'] = df['close'].rolling(20,min_periods=1).mean()
    plt.plot(pd.to_datetime(df['timestamp'], unit='ms'), df['ma5'], label='MA5')
    plt.plot(pd.to_datetime(df['timestamp'], unit='ms'), df['ma20'], label='MA20')
    plt.title(f"{r['symbol']} Intraday 5-min")
    plt.legend()
    fname = os.path.join(outdir, f"{r['symbol']}_scan.png")
    plt.savefig(fname)
    plt.close()
    print('Saved', fname)

print('Done')
