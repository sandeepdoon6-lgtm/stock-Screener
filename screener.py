# SAME CODE (short version)
from kiteconnect import KiteConnect
from datetime import datetime
import requests

api_key = "YOUR_API_KEY"
access_token = "YOUR_ACCESS_TOKEN"

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

BOT_TOKEN = "8770078207:AAEx81u3m75I2p69QStnem78L6LMSVQZNpY"
CHAT_ID = "819994547"

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": msg})

stocks = ["RELIANCE","TCS","INFY"]

msg = "🔥 Breakout Stocks:\n"

for stock in stocks:
    try:
        s = f"NSE:{stock}"
        ltp = kite.ltp(s)
        token = ltp[s]["instrument_token"]

        data = kite.historical_data(
            token,
            datetime.now().replace(hour=9, minute=15),
            datetime.now().replace(hour=9, minute=20),
            "5minute"
        )

        if not data:
            continue

        high = data[0]['high']
        low = data[0]['low']
        cmp = kite.ltp(s)[s]["last_price"]

        if cmp > high:
            msg += f"{stock} 🚀\n"
        elif cmp < low:
            msg += f"{stock} 🔻\n"

    except:
        pass

send(msg)
