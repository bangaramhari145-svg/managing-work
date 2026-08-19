#!/usr/bin/env python
"""Scan NIFTY futures intraday and rank by momentum*volume.
Usage: python trading-bot/scripts/nifty_fut_scan.py <API_KEY> <CLIENT_CODE> <PASSWORD> <TOTP>
"""
import sys
from SmartApi.smartConnect import SmartConnect
from datetime import datetime
import pandas as pd

if len(sys.argv) < 5:
    print("Usage: nifty_fut_scan.py <API_KEY> <CLIENT_CODE> <PASSWORD> <TOTP>")
    sys.exit(1)

api_key, client_code, password, totp = sys.argv[1:5]
sc = SmartConnect(api_key=api_key)
res = sc.generateSession(client_code, password, totp)
if not res.get('status'):
    print('Login failed:', res)
    sys.exit(2)

search = sc.searchScrip('NFO', 'NIFTY')
items = search.get('data', [])
# Filter FUT symbols and sort by tradingsymbol
futs = [it for it in items if 'FUT' in it.get('tradingsymbol','')]
if not futs:
    print('No FUT symbols found')
    sys.exit(3)

# pick up to 5 nearest expiries (list is not guaranteed ordered by expiry; pick first 5)
chosen = futs[:5]
results = []
for fut in chosen:
    token = str(fut['symboltoken']).split()[0]
    ts = fut['tradingsymbol']
    today = datetime.now().strftime('%Y-%m-%d')
    params = {
        'exchange': 'NFO',
        'symboltoken': token,
        'interval': 'FIVE_MINUTE',
        'fromdate': f"{today} 09:15",
        'todate': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    c = sc.getCandleData(params)
    data = c.get('data') if isinstance(c, dict) else None
    if not data:
        continue
    df = pd.DataFrame(data, columns=['timestamp','open','high','low','close','volume'])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    window = 6
    if len(df) >= window:
        mom = (df['close'].iloc[-1] - df['close'].iloc[-window]) / df['close'].iloc[-window]
        vol_sum = df['volume'].iloc[-window:].sum()
    else:
        mom = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]
        vol_sum = df['volume'].sum()
    score = mom * vol_sum
    results.append({'symbol': ts, 'token': token, 'momentum': mom, 'volume': vol_sum, 'score': score})

# sort by score desc
ranked = sorted(results, key=lambda x: x['score'], reverse=True)
print('Top NIFTY futures by momentum*volume:')
for r in ranked:
    print(f"{r['symbol']} token={r['token']} mom={r['momentum']:.6f} vol={int(r['volume'])} score={r['score']:.3f}")
