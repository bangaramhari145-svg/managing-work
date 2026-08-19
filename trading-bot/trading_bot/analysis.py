import pandas as pd
import numpy as np

def compute_momentum(df, window=6):
    # momentum: (last - last-window)/last-window
    if len(df) < window:
        return (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]
    return (df['close'].iloc[-1] - df['close'].iloc[-window]) / df['close'].iloc[-window]

def moving_averages(df, short=5, long=20):
    df['ma_short'] = df['close'].rolling(short, min_periods=1).mean()
    df['ma_long'] = df['close'].rolling(long, min_periods=1).mean()
    return df

def rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(com=period-1, adjust=False).mean()
    ma_down = down.ewm(com=period-1, adjust=False).mean()
    rs = ma_up / (ma_down + 1e-9)
    return 100 - (100 / (1 + rs))

def compute_indicators(df):
    # expects df with close and volume as floats, index in time order
    df = moving_averages(df.copy())
    df['rsi'] = rsi(df['close'])
    mom = compute_momentum(df)
    vol = df['volume'].iloc[-6:].sum() if len(df) >= 6 else df['volume'].sum()
    latest = df.iloc[-1]
    ma_signal = 1 if latest['ma_short'] > latest['ma_long'] else -1
    # RSI signal: 1 if rsi < 40 (oversold), -1 if rsi > 60 (overbought), else 0
    rsi_val = latest['rsi'] if 'rsi' in latest else np.nan
    if rsi_val < 40:
        rsi_signal = 1
    elif rsi_val > 60:
        rsi_signal = -1
    else:
        rsi_signal = 0
    return {
        'momentum': mom,
        'volume': vol,
        'ma_signal': ma_signal,
        'rsi': float(rsi_val),
        'rsi_signal': rsi_signal
    }

def score_indicator(ind):
    # Composite score: momentum*volume sign + ma_signal*abs(momentum) + rsi adjustment
    score = ind['momentum'] * ind['volume']
    score += ind['ma_signal'] * abs(ind['momentum']) * 1e3
    # modest rsi boost when oversold
    score += ind['rsi_signal'] * 1e2
    return score
