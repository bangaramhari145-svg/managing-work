#!/usr/bin/env python
"""Obtain SmartAPI access and refresh tokens using SmartApi SDK.
Usage: python trading-bot/scripts/get_tokens.py <API_KEY> <CLIENT_CODE> <PASSWORD> [TOTP]
"""
import sys
import json

try:
    from SmartApi.smartConnect import SmartConnect
except Exception as e:
    print("SmartApi SDK not installed. Install requirements and retry.")
    raise

if len(sys.argv) < 4:
    print("Usage: get_tokens.py <API_KEY> <CLIENT_CODE> <PASSWORD> [TOTP]")
    sys.exit(1)

api_key = sys.argv[1]
client_code = sys.argv[2]
password = sys.argv[3]
totp = sys.argv[4] if len(sys.argv) > 4 else None

sc = SmartConnect(api_key=api_key)
try:
    res = sc.generateSession(client_code, password, totp)
except Exception as e:
    print(f"generateSession failed: {e}")
    sys.exit(2)

# Print token info (copy these to GitHub Secrets)
print(json.dumps(res, indent=2))
