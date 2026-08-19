Setting up TOTP for SmartAPI (Angel One)

1) Developer access
   - Log in to SmartAPI / Angel One developer portal: https://smartapi.angelbroking.com or https://apiconnect.angelbroking.com
   - Go to "My Apps" or "API Keys" and select the application/API key you registered.

2) Locate TOTP / 2FA secret
   - Look for a section labeled "TOTP", "2FA", "Auth Token", or "QR code" for API access.
   - If you see a QR code, scan it with Google Authenticator, Authy, or another TOTP app.
   - If you see a text secret key, copy it into your TOTP app as a manual entry.

3) Get a 6-digit code
   - Open your authenticator app and read the current 6-digit code for the SmartAPI entry.
   - Use this 6-digit code as the totp parameter when calling the generateSession API (or when running trading-bot/scripts/get_tokens.py).

4) If you cannot find TOTP settings
   - Some accounts require contacting Angel One support to enable API/TOTP for SmartAPI access. Reach out to Angel One support or your RM and request SmartAPI access + TOTP activation.

5) After generating tokens
   - Copy the response's jwtToken and refreshToken into your GitHub Secrets (ANGEL_ACCESS_TOKEN, ANGEL_REFRESH_TOKEN) or a local .env file.
   - Keep these tokens secret. If accidentally exposed, rotate/revoke immediately.

Notes
 - Use PAPER_MODE=true for testing so real orders are not placed.
 - The trading-bot includes scripts/get_tokens.py to call generateSession with API_KEY, client_code and password + totp when required.
