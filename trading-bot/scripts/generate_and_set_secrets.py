#!/usr/bin/env python
"""Generate jwt/refresh tokens via SmartAPI and store them as GitHub Secrets using gh CLI.
Usage: python generate_and_set_secrets.py <API_KEY> <CLIENT_CODE> <PASSWORD> <TOTP>

This script will NOT print tokens; it will call gh secret set to store them.
"""
import sys
import json
import subprocess

try:
    from SmartApi.smartConnect import SmartConnect
except Exception as e:
    print("SmartApi SDK not installed. Install requirements and retry.")
    raise

if len(sys.argv) < 5:
    print("Usage: generate_and_set_secrets.py <API_KEY> <CLIENT_CODE> <PASSWORD> <TOTP>")
    sys.exit(1)

api_key, client_code, password, totp = sys.argv[1:5]

sc = SmartConnect(api_key=api_key)
try:
    res = sc.generateSession(client_code, password, totp)
except Exception as e:
    print(f"generateSession failed: {e}")
    sys.exit(2)

if not res or not res.get('status'):
    print(f"generateSession response indicates failure: {res}")
    sys.exit(3)

data = res.get('data', {})
jwt = data.get('jwtToken')
refresh = data.get('refreshToken')

if not jwt or not refresh:
    print("Did not receive tokens from SmartAPI. Response data:\n" + json.dumps(data))
    sys.exit(4)

# Set GitHub secrets using gh CLI
def gh_set(name, value):
    try:
        subprocess.check_call(["gh", "secret", "set", name, "--body", value])
    except subprocess.CalledProcessError as e:
        print(f"Failed to set secret {name}: {e}")
        sys.exit(5)

gh_set('ANGEL_ACCESS_TOKEN', jwt)
gh_set('ANGEL_REFRESH_TOKEN', refresh)
gh_set('ANGEL_ACCOUNT_ID', client_code)

print("TOKENS_STORED_AS_SECRETS")
